from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def root():
    return 'Root page'

# Projects
@app.route('/projects')
def projects():
    # TODO: Simulate getting data for different groupings and rendering it
    print '==> %s' % request.args.get('group', None)
    search_project = {'title': 'Search', 'target_date': 'Feb 15, 2012', 'est_date': 'Feb 10, 2012',
        'detail_url': '/projects/1',
        'key_dates': [['Integration with PAL', 'Dec 15, 2012']]}
    return render_template('projects.html', projects=[search_project])

@app.route('/projects/<int:project_id>')
def project(project_id):
    return 'Details for project %s' % project_id

@app.route('/projects/new')
def projects_new():
    return 'Create a new project'

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

