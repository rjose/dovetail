from flask import Flask, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database
import dovetail.projects.views

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

# Project routes
app.register_blueprint(dovetail.projects.views.mod)

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

