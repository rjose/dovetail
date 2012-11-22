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
            {'name': 'Do more work', 'is_key': True, 'assignee': rino},
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

# People
@app.route('/people')
def people():
    return 'List of all People'

@app.route('/people/new')
def people_new():
    return 'Create new person'

if __name__ == '__main__':
    # TODO: Figure out how to set this via an environment variable
    app.run(debug=True)

