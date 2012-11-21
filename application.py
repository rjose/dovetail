from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def root():
    return 'Root page'

# Projects
@app.route('/projects')
def projects():
    return render_template('projects.html')

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

