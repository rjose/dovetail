from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('projects'))

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
        # TODO: Implement the creation of the project
        print "==> Project name: %s" % request.form['name']
        return redirect(url_for('project', project_id=2))
    else:
        # TODO: Simulate getting data for different groupings and rendering it
        print '==> %s' % request.args.get('group', None)
        return render_template('projects.html', projects=get_phony_project_data())

@app.route('/projects/<int:project_id>')
def project(project_id):
    return render_template('project_details.html',
            project_details=get_project_details(project_id))

@app.route('/projects/new')
def projects_new():
    return render_template('projects_new.html')

@app.route('/projects/edit')
def projects_edit():
    return 'Editing projects'

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
    project = {'project_id': project_id, 'name': 'Endorsements'}
    return render_template('project_participants_new.html', project=project)

@app.route('/projects/<int:project_id>/participants', methods=['POST'])
def project_participants(project_id):
    if request.method == 'POST':
        # TODO: Implement the creation of a participant
        print "==> Participant name: %s" % request.form['name']
        print "==> Participant picture: %s" % request.form['picture']
        print "==> Participant team: %s" % request.form['team']
        return redirect(url_for('project', project_id=project_id))
    else:
        return "TODO: Figure out what should go here"

# People
@app.route('/people')
def people():
    return 'List of all People'

@app.route('/people/new')
def people_new():
    return 'Create new person'

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

