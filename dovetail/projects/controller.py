from flask import Blueprint, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.util
import dovetail.database as database
import dovetail.projects.db as projects_db
import dovetail.work.db as work_db
from dovetail.projects.util import project_work_to_string, parse_workline

from dovetail.scheduler import Scheduler
from dovetail.projects.project import get_projects_for_scheduling

mod = Blueprint('projects', __name__)

# Projects
@mod.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        target_date = dovetail.util.parse_date(request.form['target_date'])
        projects_db.insert_project(g.connection, request.form['name'], target_date)
    else:
        pass
    return render_template('projects/collection.html',
            database = database,
            projects = projects_db.select_project_collection(g.connection))

@mod.route('/projects/<int:project_id>')
def project(project_id):
    return render_template('projects/details.html',
            database = database,
            project_details = projects_db.select_project(g.connection, project_id))

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
    return render_template('projects/edit_work.html',
            project = project,
            work_data = project_work_to_string(project.get('work', [])))

@mod.route('/projects/<int:project_id>/work', methods = ['POST'])
def project_work(project_id):
    worklines = request.form['work'].split('\n')
    for workline in worklines:
        try:
            work_data = parse_workline(g.connection, workline)
            fields = work_data['fields']
            fields.update(project_id = project_id)
            work_db.update_work(g.connection, work_data)
        except:
            # TODO: Log something
            pass
    return redirect('/projects/%d' % int(project_id))

@mod.route('/projects/<int:project_id>/participants/new')
def project_participants_new(project_id):
    project = projects_db.select_project(g.connection, project_id)
    return render_template('projects/new_participant.html',
            project = project,
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
    scheduler = Scheduler(datetime.now())
    projects = get_projects_for_scheduling(g.connection)
    projects = scheduler.schedule_projects(projects)
    projects_db.update_project_and_work_dates(g.connection, projects)
    return redirect('/projects')

