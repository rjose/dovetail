from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return 'Root page'

def get_phony_project_data():
    # TODO: Read this from a database
    search_project = {'title': 'Search', 'target_date': 'Feb 15, 2012', 'est_date': 'Feb 10, 2012',
        'detail_url': '/projects/1',
        'key_dates': [['Integration with PAL', 'Dec 15, 2012']]}
    endorsements_project = {'title': 'Endorsements', 'target_date': 'Mar 15, 2012', 'est_date': 'Mar 20, 2012',
        'detail_url': '/projects/2',
        'key_dates': []}
    rich_media_project = {'title': 'Rich Media', 'target_date': 'Mar 15, 2012', 'est_date': 'Mar 2, 2012',
        'detail_url': '/projects/3',
        'key_dates': []}
    mentions_project = {'title': 'Mentions', 'target_date': 'Mar 25, 2012', 'est_date': 'Mar 25, 2012',
        'detail_url': '/projects/4',
        'key_dates': []}
    return [search_project, endorsements_project, rich_media_project, mentions_project]

# Projects
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        # TODO: Implement the creation of the project
        return redirect(url_for('project', project_id=2))
    else:
        # TODO: Simulate getting data for different groupings and rendering it
        print '==> %s' % request.args.get('group', None)
        return render_template('projects.html', projects=get_phony_project_data())

@app.route('/projects/<int:project_id>')
def project(project_id):
    return 'Details for project %s' % project_id

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

