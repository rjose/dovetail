from flask import Blueprint, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database
import dovetail.projects.models as models

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
    project = {'project_id': project_id, 'project_name': 'Endorsements',
            'participants': [
                {'name': 'Rino Jose', 'title': "Engineering Manager", 'team': 'Mobile'}
            ] }
    work_data = "[240, 'BB', '0.1d', 'A prerequisite', [], 'Dec 20, 2012']\n"
    work_data += "[320, 'RJ', '1d', 'Another prerequisite', [], '']\n"
    work_data += "[121, 'RJ', '2.5d', 'Figure out thing for thing', [240, 320], '']\n"
    return render_template('projects/edit_work.html', project=project, work_data = work_data)

@mod.route('/projects/<int:project_id>/work', methods = ['POST'])
def project_work(project_id):
    # TODO: Update this work
    return redirect(url_for('project', project_id=project_id))

@mod.route('/projects/<int:project_id>/participants/new')
def project_participants_new(project_id):
    people_data = g.connection.execute('select id, name from people order by name')
    people = [{'id': row['id'], 'name': row['name']} for row in people_data]
    project = models.get_project_details(g.connection, project_id)
    return render_template('projects/new_participant.html', project=project,
            people = people)

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
