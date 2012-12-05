from flask import Blueprint, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database
import dovetail.people.db as people_db
import dovetail.work.db as work_db
import dovetail.util

mod = Blueprint('people', __name__)

@mod.route('/people', methods=['GET', 'POST'])
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
    return render_template('people/collection.html', people = people)


@mod.route('/people/<int:person_id>')
def person_details(person_id):
    person = people_db.select_person(g.connection, person_id)
    work = work_db.select_work_for_person(g.connection, person_id)
    for w in work:
        w.effort_left_d = dovetail.util.format_effort_left(w.effort_left_d)
        w.est_end_date = dovetail.util.format_date(w.end_date)
        w.key_date = dovetail.util.format_date(w.key_date)
        w.project_url = '/projects/%d' % int(w.project_id)
    person.work = work
    return render_template('people/details.html', person = person)

@mod.route('/people/new')
def people_new():
    return render_template('people/new.html')

