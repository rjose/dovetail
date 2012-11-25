from flask import Blueprint, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database
import dovetail.projects.models as models
import dovetail.work.models as work

mod = Blueprint('projects', __name__)

# Projects
@mod.route('/projects', methods=['GET', 'POST'])
def projects_route():
    if request.method == 'POST':
        target_date = datetime.strptime(request.form['target_date'], "%b %d, %Y")
        g.connection.execute(database.projects.insert(),
               name = request.form['name'],
               target_date = target_date)
    else:
        pass
    return render_template('projects/collection.html',
            projects = models.get_projects_data(g.connection))

@mod.route('/projects/<int:project_id>')
def project(project_id):
    return render_template('projects/details.html',
            project_details = models.get_project_details(g.connection, project_id))

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
    project = models.get_project_details(g.connection, project_id)
    return render_template('projects/edit_work.html',
            project = project,
            work_data = models.work_to_string(project.get('work', [])))

@mod.route('/projects/<int:project_id>/work', methods = ['POST'])
def project_work(project_id):
    # TODO: Do some error handling here
    worklines = request.form['work'].split('\n')
    for workline in worklines:
        work_data = models.parse_workline(g.connection, workline)
        fields = work_data['fields']
        fields.update(project_id = project_id)

        # Update the work table
        statement = database.work.update().\
            where(database.work.c.id == work_data['id']).\
            values(fields)
        g.connection.execute(statement)
    return redirect('/projects/%d' % int(project_id))

@mod.route('/projects/<int:project_id>/participants/new')
def project_participants_new(project_id):
    project = models.get_project_details(g.connection, project_id)
    return render_template('projects/new_participant.html',
            project = project,
            people = database.get_people(g.connection))

@mod.route('/projects/<int:project_id>/participants', methods=['POST'])
def project_participants(project_id):
    if request.method == 'POST':
        g.connection.execute(database.project_participants.insert(),
               project_id = project_id,
               person_id = request.form['person']
               )
        return redirect(url_for('project', project_id=project_id))
    else:
        return "TODO: Figure out what should go here"
