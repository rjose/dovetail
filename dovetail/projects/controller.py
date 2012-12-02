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
    for p in projects:
        d = {
                'project_id': p.project_id,
                'name': p.name,
                'target_date': dovetail.util.format_date(p.target_date),
                'est_end_date': dovetail.util.format_date(p.est_end_date),
                'detail_url': '/projects/%d' % p.project_id,
                'key_work': [{
                    'date': dovetail.util.format_date(w.key_date),
                    'title': w.title
                    } for w in work_db.select_key_work_for_project(g.connection, p.project_id)]
            }
        data.append(d)
        project_rank_data.append('%d %s' % (p.project_id, p.name))

    return render_template('projects/collection.html', project_data = data,
            project_rank_data = '\n'.join(project_rank_data))

@mod.route('/projects/<int:project_id>')
def project(project_id):
    project = projects_db.select_project(g.connection, project_id)
    for w in project.work:
        w.key_date = dovetail.util.format_date(w.key_date)
    project_data = {
            'project_id': project.project_id,
            'name': project.name,
            'target_date': dovetail.util.format_date(project.target_date),
            'est_end_date': dovetail.util.format_date(project.est_end_date),
            'total_effort': dovetail.util.format_effort_left(project.total_effort()),
            'work': project.work,
            'participants': project.participants
            }

    return render_template('projects/details.html',
            project_data = project_data,
            work_data = projects_util.project_work_to_string(project.work),
            participants = people_db.select_project_participants(g.connection, project_id),
            people = people_db.select_people(g.connection))

@mod.route('/projects/edit', methods = ['GET', 'POST'])
def projects_edit():
    if request.method == 'GET':
        project_data = "1 Search\n"
        project_data += "2 Endorsements\n"
        project_data += "3 Rich Media\n"
        project_data += "4 Mentions\n"
        return render_template('projects/edit_collection.html', project_data=project_data)
    else:
        # TODO: Update the rankings
        return redirect(url_for('projects'))

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

