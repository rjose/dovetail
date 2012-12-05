from datetime import datetime
from flask import (Blueprint, Response, json, render_template, request,
                   redirect, url_for, g)

import dovetail.util
import dovetail.projects.db as projects_db
import dovetail.work.db as work_db
import dovetail.people.db as people_db
import dovetail.projects.util as projects_util
import dovetail.scheduler

from dovetail.projects.project import Project
from dovetail.work.work import Work

mod = Blueprint('projects', __name__)

# Projects
@mod.route('/projects')
def projects():
    projects = projects_db.select_project_collection(g.connection)
    data = []
    project_rank_data = []
    for i, p in enumerate(projects):
        d = {
                'project_id': p.project_id,
                'rank': i + 1,
                'name': p.name,
                'target_date': dovetail.util.format_date(p.target_date),
                'est_end_date': dovetail.util.format_date(p.est_end_date),
                'status': projects_util.compute_status(p.target_date, p.est_end_date),
                'effort_left_d': dovetail.util.format_effort_left(p.total_effort(), 0),
                'detail_url': '/projects/%d' % p.project_id,
                'key_work': [{
                    'date': dovetail.util.format_date(w.key_date),
                    'title': w.title
                    } for w in work_db.select_key_work_for_project(g.connection, p.project_id)]
            }
        data.append(d)
        project_rank_data.append('%d %s' % (p.project_id, p.name))

    project_ids = json.dumps([p.project_id for p in projects])

    done_projects = projects_db.select_done_project_collection(g.connection)
    return render_template('projects/collection.html',
            project_data = data,
            project_rank_data = '\n'.join(project_rank_data),
            project_ids = project_ids,
            done_projects = done_projects)

# TODO: Move this
def format_work_dates(work_collection):
    for w in work_collection:
        w.key_date = dovetail.util.format_date(w.key_date)
    return

@mod.route('/projects/<int:project_id>')
def project(project_id):
    project = projects_db.select_project(g.connection, project_id)
    format_work_dates(project.work)
    project_data = {
            'project_id': project.project_id,
            'name': project.name,
            'target_date': dovetail.util.format_date(project.target_date),
            'est_end_date': dovetail.util.format_date(project.est_end_date),
            'status': projects_util.compute_status(project.target_date, project.est_end_date),
            'effort_left_d': dovetail.util.format_effort_left(project.total_effort(), 1),
            'work': project.work,
            'work_ids': json.dumps([w.work_id for w in project.work]),
            'participants': project.participants
            }
    done_work = work_db.select_done_work_for_project(g.connection, project_id)
    format_work_dates(done_work)

    return render_template('projects/details.html',
            project_data = project_data,
            work_data = projects_util.project_work_to_string(project.work),
            participants = people_db.select_project_participants(g.connection, project_id),
            done_work = done_work,
            people = people_db.select_people(g.connection))

# TODO: Move this
def to_work(fields):
    result = Work(fields['id'], fields['title'], fields['effort_left_d'],
            dovetail.util.condition_prereqs(fields['prereqs']),
            fields['assignee_id'], fields['key_date'])
    return result


@mod.route('/api/projects/<int:project_id>', methods=['POST'])
def edit_project(project_id):
    name = request.values['name']
    target_date = dovetail.util.parse_date(request.values['target_date'])
    worklines = request.values['worklines'].split('\n')
    original_work_ids = set(json.loads(request.values['original_work_ids']))

    work = []
    for workline in worklines:
        try:
            # TODO: Change these so they return Work objects
            work_data = projects_util.parse_workline(g.connection, workline)
            fields = work_data['fields']
            fields.update(project_id = project_id)

            # Save any changes to the work items
            # TOOD: Separate topo sort work so we only have to write to database once
            work_db.update_work(g.connection, work_data)
            fields.update(id = work_data['id'])
            work.append(to_work(fields))
        except:
            # TODO: log something
            pass

    # Mark missing work as done
    returned_work_ids = set([w.work_id for w in work])
    done_work_ids = original_work_ids - returned_work_ids
    work_db.mark_work_done(g.connection, done_work_ids)

    project = Project(project_id)
    project.name = name
    project.target_date = target_date
    project.work = work
    project.topo_sort_work()
    work_db.update_work_topo_order(g.connection, project.work)
    dovetail.scheduler.reschedule_world(g.connection)

    # Update project info
    projects_db.update_project(g.connection, project)

    response_data = {}
    result = Response(json.dumps(response_data), status=200, mimetype='application/json')
    return result

@mod.route('/api/projects', methods=['POST'])
def api_add_project():
    target_date = dovetail.util.parse_date(request.values['target_date'])
    insert_result = projects_db.insert_project(g.connection,
            request.values['name'], target_date)
    response_data = {'project_id': insert_result.inserted_primary_key}
    return Response(json.dumps(response_data), status=200, mimetype='application/json')

@mod.route('/api/projects/<int:project_id>/participants', methods=['POST'])
def api_add_project_participant(project_id):
    person_id = int(request.values['person_id'])
    projects_db.add_project_participant(g.connection, project_id, person_id)
    response_data = {}
    return Response(json.dumps(response_data), status=200, mimetype='application/json')

# TODO: Move this
def parse_project_line(line, value):
    parts = line.split()
    result = Project(parts[0])
    result.value = value
    return result

@mod.route('/api/projects/rankings', methods=['POST'])
def rank_projects():
    project_lines = request.values['project_lines'].split('\n')
    original_project_ids = set(json.loads(request.values['original_project_ids']))

    # TODO: Figure out how to compute project value
    cur_value = 100
    projects = []
    for line in project_lines:
        try:
            p = parse_project_line(line, cur_value)
            cur_value -= 1
            projects.append(p)
        except:
            # TODO: log something
            pass

    # Returned project ids
    returned_project_ids = set([int(p.project_id) for p in projects])
    done_project_ids = original_project_ids - returned_project_ids
    projects_db.mark_projects_done(g.connection, done_project_ids)

    # Update project info
    projects_db.update_project_collection_value(g.connection, projects)
    dovetail.scheduler.reschedule_world(g.connection)

    response_data = {}
    result = Response(json.dumps(response_data), status=200, mimetype='application/json')
    return result

@mod.route('/projects/reschedule', methods=['POST'])
def reschedule_projects():
    dovetail.scheduler.reschedule_world(g.connection)
    return redirect('/projects')

@mod.route('/api/project/<int:project_id>/mark_undone', methods=['POST'])
def api_mark_projects_undone(project_id):
    projects_db.mark_projects_undone(g.connection, [project_id])
    response_data = {}
    result = Response(json.dumps(response_data), status=200, mimetype='application/json')
    return result
