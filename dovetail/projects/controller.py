from flask import Blueprint, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database
import dovetail.projects.db as projects_db
import dovetail.work.models as work

mod = Blueprint('projects', __name__)

def shorten_name(name):
    return name

def format_prereqs(prereqs):
    if prereqs:
        return prereqs
    else:
        return "[]"


def project_work_to_string(work_data):
    # TODO: Delete this example data
    # work_data = "[240, 'BB', '0.1d', 'A prerequisite', [], 'Dec 20, 2012']\n"
    # work_data += "[320, 'RJ', '1d', 'Another prerequisite', [], '']\n"
    # work_data += "[121, 'RJ', '2.5d', 'Figure out thing for thing', [240, 320], '']\n"
    result = ''
    for w in work_data:
        result += '[%d, "%s", "%s", "%s", %s, "%s"]\n' % (
                w['id'],
                shorten_name(w['assignee']['name']),
                work.format_effort_left(w['effort_left_d']),
                w['title'],
                format_prereqs(w['prereqs']),
                database.format_date(w['key_date']))
    return result

def parse_workline(connection, workline):
    data = json.loads(workline)
    # TODO: Do some error handling here
    person = people.get_person_from_name(connection, data[1])
    effort_left_d = float(data[2].split()[0])
    key_date = None
    if data[5] != '?':
        key_date = database.parse_date(data[5])

    result = {
            'id': data[0],
            'fields': {
                'assignee_id': person['id'],
                'effort_left_d': effort_left_d,
                'title': data[3],
                'prereqs': str(data[4]),
                'key_date': key_date
                }
            }
    return result


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

            # Update the work table
            statement = database.work.update().\
                where(database.work.c.id == work_data['id']).\
                values(fields)
            g.connection.execute(statement)
        except:
            # TODO: Log someething
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
        g.connection.execute(database.project_participants.insert(),
               project_id = project_id,
               person_id = request.form['person']
               )
        return redirect(url_for('project', project_id=project_id))
    else:
        return "TODO: Figure out what should go here"
