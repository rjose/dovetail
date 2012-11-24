from flask import Flask, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database
import dovetail.projects.views
import dovetail.people.views

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
    return redirect('/projects')

# Register blueprints
app.register_blueprint(dovetail.people.views.mod)
app.register_blueprint(dovetail.projects.views.mod)


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

