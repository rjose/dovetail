from flask import Flask, render_template, request, redirect, url_for, g
import dovetail.database as database
from datetime import datetime

database.metadata.create_all()

app = Flask(__name__)

@app.before_request
def open_connection():
    g.connection = database.engine.connect()

@app.teardown_request
def close_connection(exeption=None):
    g.connection.close()

@app.route('/')
def root():
    return redirect(url_for('projects'))

# TODO: Move this to the database.py file
def format_date(date):
    if date == None:
        return "?"
    else:
        return datetime.strftime(date, "%b %d, %Y")

def get_projects_data():
    data = g.connection.execute(database.projects.select())
    result = []
    for row in data:
        format_date(row['est_date'])
        p = {
                'project_id': row['id'],
                'title': row['name'],
                'target_date': format_date(row['target_date']),
                'est_date': format_date(row['est_date']),
                'detail_url': '/projects/%d' % row['id'],
                'key_dates': []
            }
        result.append(p)
    return result + get_phony_project_data()

# TODO: Delete this
def get_phony_project_data():
    # TODO: Read this from a database
    search_project = {'project_id': 1,
        'title': 'Search',
        'target_date': 'Feb 15, 2012',
        'est_date': 'Feb 10, 2012',
        'detail_url': '/projects/1',
        'key_dates': [['Integration with PAL', 'Dec 15, 2012']]}
    endorsements_project = {'project_id': 2,
        'title': 'Endorsements',
        'target_date': 'Mar 15, 2012',
        'est_date': 'Mar 20, 2012',
        'detail_url': '/projects/2',
        'key_dates': []}
    rich_media_project = {'project_id': 3,
        'title': 'Rich Media',
        'target_date': 'Mar 15, 2012',
        'est_date': 'Mar 2, 2012',
        'detail_url': '/projects/3',
        'key_dates': []}
    mentions_project = {'project_id': 4,
        'title': 'Mentions',
        'target_date': 'Mar 25, 2012',
        'est_date': 'Mar 25, 2012',
        'detail_url': '/projects/4',
        'key_dates': []}
    return [search_project, endorsements_project, rich_media_project, mentions_project]

def get_project_details(project_id):
    particpants_data = g.connection.execute(
            '''select id, name, title, team, picture from people
               inner join project_participants on project_participants.person_id = people.id
               where project_participants.project_id=1
               order by name''')
    participants = [{'id': p['id'], 'name': p['name'], 'title': p['title'],
        'team': p['team'], 'picture': p['picture']}
            for p in particpants_data]
    data = g.connection.execute(database.projects.select(
        database.projects.c.id == project_id)).first()
    result = {
        'project_id': data['id'],
        'name': data['name'],
        'stats': {
            'target_date': format_date(data['target_date']),
            'est_date': format_date(data['est_date']),
            'total_effort': 'TODO',
            },
        'participants': participants,
        'work': [
            ]
        }

    return result

def get_phony_project_details(project_id):
    rino = {'name': 'Rino Jose',
            'picture': 'https://m1-s.licdn.com/mpr/mpr/shrink_80_80/p/2/000/019/20e/2464c31.jpg'}
    result = {
        'project_id': 2,
        'name': 'Endorsements',
        'stats': {
            'target_date': 'Mar 15, 2012',
            'est_date': 'Mar 20, 2012',
            'total_effort': '40 man-days',
            },
        'participants': [
            {'name': 'Rino Jose', 'title': "Engineering Manager", 'team': 'Mobile'}
            ],
        'work': [
            {'name': 'Figure out the thing for the thing', 'is_done': 'Done: Oct 14, 2012',
                'assignee': rino},
            {'name': 'Do the actual work', 'assignee': rino},
            {'name': 'Do more work', 'key_date': 'Dec 19, 2012', 'assignee': rino},
            ]
        }
    return result

# Projects
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        target_date = datetime.strptime(request.form['target_date'], "%b %d, %Y")
        g.connection.execute(database.projects.insert(),
               name = request.form['name'],
               target_date = target_date)
    else:
        pass
    return render_template('projects.html', projects=get_projects_data())

@app.route('/projects/<int:project_id>')
def project(project_id):
    return render_template('project_details.html',
            project_details=get_project_details(project_id))

@app.route('/projects/new')
def projects_new():
    return render_template('projects_new.html')

@app.route('/projects/edit', methods = ['GET', 'POST'])
def projects_edit():
    if request.method == 'GET':
        project_data = "1 Search\n"
        project_data += "2 Endorsements\n"
        project_data += "3 Rich Media\n"
        project_data += "4 Mentions\n"
        return render_template('projects_edit.html', project_data=project_data)
    else:
        # TODO: Update the rankings
        return redirect(url_for('projects'))

@app.route('/projects/<int:project_id>/work/edit')
def project_work_edit(project_id):
    project = {'project_id': project_id, 'project_name': 'Endorsements',
            'participants': [
                {'name': 'Rino Jose', 'title': "Engineering Manager", 'team': 'Mobile'}
            ] }
    work_data = "[240, 'BB', '0.1d', 'A prerequisite', [], 'Dec 20, 2012']\n"
    work_data += "[320, 'RJ', '1d', 'Another prerequisite', [], '']\n"
    work_data += "[121, 'RJ', '2.5d', 'Figure out thing for thing', [240, 320], '']\n"
    return render_template('project_work_edit.html', project=project, work_data = work_data)

@app.route('/projects/<int:project_id>/work', methods = ['POST'])
def project_work(project_id):
    # TODO: Update this work
    return redirect(url_for('project', project_id=project_id))

@app.route('/projects/<int:project_id>/participants/new')
def project_participants_new(project_id):
    people_data = g.connection.execute('select id, name from people order by name')
    people = [{'id': row['id'], 'name': row['name']} for row in people_data]
    project = get_project_details(project_id)
    return render_template('project_participants_new.html', project=project,
            people = people)

@app.route('/projects/<int:project_id>/participants', methods=['POST'])
def project_participants(project_id):
    if request.method == 'POST':
        g.connection.execute(database.project_participants.insert(),
               project_id = project_id,
               person_id = request.form['person']
               )
        return redirect(url_for('project', project_id=project_id))
    else:
        return "TODO: Figure out what should go here"

# People
@app.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'POST':
        g.connection.execute(database.people.insert(),
               name = request.form['name'],
               title = request.form['title'],
               team = request.form['team'],
               picture = request.form['picture'])
    else:
        pass
    people_data = g.connection.execute('select id, name from people')
    people = [{'id': p['id'], 'name': p['name']} for p in people_data]
    return render_template('people.html', people = people)

@app.route('/people/new')
def people_new():
    return render_template('people_new.html')

# Work
@app.route('/work', methods=['GET', 'POST'])
def work():
    if request.method == 'POST':
        # TODO: Implement the creation of the work
        print "==> Work name: %s" % request.form['name']
        print "==> Work assignee: %s" % request.form['assignee']
        print "==> Work estimate: %s" % request.form['estimate']
        project_id = request.args.get('project', None)
        return redirect(url_for('project', project_id=project_id))
    else:
        return "TODO: Figure out what should go here"


@app.route('/work/new')
def work_new():
    project_id = request.args.get('project', 0)

    # TODO: Do some error handling if we don't have a project id
    project = {'project_name': 'Endorsements', 'project_id': project_id}
    return render_template('work_new.html', project=project)

if __name__ == '__main__':
    # TODO: Figure out how to set this via an environment variable
    app.run(debug=True)

