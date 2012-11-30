from flask import Blueprint, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.util
import dovetail.database as database
import dovetail.projects.db as projects_db
import dovetail.work.db as work_db
from dovetail.projects.util import project_work_to_string, parse_workline
from dovetail.projects.project import Project
from dovetail.work.work import Work

from dovetail.scheduler import Scheduler

mod = Blueprint('projects', __name__)

def reschedule_world(connection):
    scheduler = Scheduler(datetime.now())
    projects = projects_db.get_projects_for_scheduling(connection)
    projects = scheduler.schedule_projects(projects)
    projects_db.update_project_and_work_dates(connection, projects)
    return

# Projects
@mod.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        target_date = dovetail.util.parse_date(request.form['target_date'])
        projects_db.insert_project(g.connection, request.form['name'], target_date)
    else:
        pass
    # TODO: Change this when we update select_project_collection
    return render_template('projects/collection.html',
            database = dovetail.util,
            projects = projects_db.select_project_collection(g.connection))

@mod.route('/projects/<int:project_id>')
def project(project_id):
    project = projects_db.select_project(g.connection, project_id)
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
            database = dovetail.util,
            project_data = project_data)

@mod.route('/projects/new')
def projects_new():
    return render_template('projects/new.html')

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

@mod.route('/projects/<int:project_id>/work/edit')
def project_work_edit(project_id):
    project = projects_db.select_project(g.connection, project_id)
    project_data = {
            'project_id': project.project_id,
            'name': project.name,
            'participants': project.participants,
            'work': project_work_to_string(project.work)
            }
    return render_template('projects/edit_work.html', project_data = project_data)

# TODO: Move this
def to_work(fields):
    result = Work(fields['id'], fields['title'], fields['effort_left_d'],
            dovetail.util.condition_prereqs(fields['prereqs']),
            fields['assignee_id'], fields['key_date'])
    return result

@mod.route('/projects/<int:project_id>/work', methods = ['POST'])
def project_work(project_id):
    worklines = request.form['work'].split('\n')
    work = []
    for workline in worklines:
        # We have this here to skip lines that cannot be parsed (like empty lines)
        try:
            # TODO: Change these so they return Work objects
            work_data = parse_workline(g.connection, workline)
            fields = work_data['fields']
            fields.update(project_id = project_id)
            work_db.update_work(g.connection, work_data)
            fields.update(id = work_data['id'])
            work.append(to_work(fields))
        except:
            pass

    project = Project(project_id)
    project.work = work
    project.topo_sort_work()
    work_db.update_work_topo_order(g.connection, project.work)

    reschedule_world(g.connection)
    return redirect('/projects/%d' % int(project_id))

@mod.route('/projects/<int:project_id>/participants/new')
def project_participants_new(project_id):
    project = projects_db.select_project(g.connection, project_id)
    project_data = {
            'project_id': project.project_id,
            'name': project.name
            }
    return render_template('projects/new_participant.html',
            project_data = project_data,
            people = database.get_people(g.connection))

@mod.route('/projects/<int:project_id>/participants', methods=['POST'])
def project_participants(project_id):
    if request.method == 'POST':
        projects_db.add_project_participant(g.connection, project_id, request.form['person'])
        return redirect('/projects/%d' % int(project_id))
    else:
        return "TODO: Figure out what should go here"

@mod.route('/projects/reschedule', methods=['POST'])
def reschedule_projects():
    reschedule_world(g.connection)
    return redirect('/projects')

