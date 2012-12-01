from flask import Blueprint, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database
import dovetail.projects.db as projects_db
import dovetail.people.db as people_db

mod = Blueprint('work', __name__)

@mod.route('/work', methods=['GET', 'POST'])
def work():
    if request.method == 'POST':
        project_id = int(request.args.get('project', None))
        g.connection.execute(database.work.insert(),
               title = request.form['title'],
               assignee_id = request.form['assignee'],
               project_id = project_id,
               effort_left_d = request.form['estimate'])
        return redirect('/projects/%d' % project_id)
    else:
        return "TODO: Figure out what should go here"


@mod.route('/work/new')
def work_new():
    project_id = request.args.get('project', 0)

    project = projects_db.select_project(g.connection, project_id)
    return render_template('work/new.html', 
            project = project,
            people = people_db.get_people(g.connection))

