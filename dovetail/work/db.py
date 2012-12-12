from datetime import datetime
import json
import dovetail.util
import dovetail.database as database
from dovetail.work.work import Work
from dovetail.people.person import Person

def fields_to_work_object(fields):
    result = Work(fields['id'])
    for f in fields.keys():
        if f == 'title':
            result.title = fields[f]
        elif f == 'assignee_id' or f == 'person_id':
            result.assignee_id = fields[f]
        elif f == 'project_name':
            result.project_name = fields[f]
        elif f == 'project_id':
            result.project_id = fields[f]

        elif f == 'effort_left_d':
            result.effort_left_d = float(fields[f])
        elif f == 'prereqs':
            result.prereqs = dovetail.util.condition_prereqs(fields[f])

        elif f == 'key_date':
            result.key_date = dovetail.util.condition_date(fields[f])
        elif f == 'start_date':
            result.start_date = dovetail.util.condition_date(fields[f])
        elif f == 'end_date':
            result.end_date = dovetail.util.condition_date(fields[f])
    return result

def work_data_to_work_object(work_data):
    result = []
    for w in work_data:
        work = fields_to_work_object(w)
        work.start_date = dovetail.util.condition_date(w['start_date'])
        work.end_date = dovetail.util.condition_date(w['end_date'])

        assignee = Person(w['person_id'])
        assignee.name = w['assignee_name']
        assignee.picture = w['assignee_picture']

        # TODO: The controller should do this
        assignee.detail_url = '/people/%d' % w['person_id']
        work.assignee = assignee
        result.append(work)
    return result

# This augments work with an assignee Person object
def select_work_for_project(connection, project_id):
    work_data = connection.execute(
            '''select w.id, w.title, w.start_date, w.end_date,
               people.id as person_id, people.name as assignee_name,
               people.picture as assignee_picture, w.effort_left_d, w.key_date, w.prereqs
               from work as w
               inner join people on people.id = w.assignee_id
               where w.project_id = %d and w.is_done = 0
               order by topo_order ASC
            ''' % int(project_id))

    result = work_data_to_work_object(work_data)
    return result

def select_work_for_person(connection, person_id):
    work_data = connection.execute(
            '''select w.id, w.title, w.effort_left_d, w.key_date, w.start_date, w.end_date,
               w.prereqs, w.project_id, w.assignee_id,
               projects.name as project_name
               from work as w
               inner join projects on projects.id = w.project_id
               where w.assignee_id = %d and w.is_done = 0
               order by w.start_date ASC
            ''' % int(person_id))
    result = [fields_to_work_object(w) for w in work_data]
    return result

def select_timelines_for_people(connection, people_ids):
    # This converts something like 'set([1, 2]) to '1, 2'
    people_id_string = str(people_ids)[5:-2]
    if not people_id_string:
        return []
    work_data = connection.execute(
            '''select w.id, w.title, w.key_date, w.start_date, w.end_date, w.key_date as work_key_date,
               w.project_id, w.effort_left_d,
               projects.name as project_name,
               people.name as assignee_name
               from work as w
               inner join projects on projects.id = w.project_id
               inner join people on people.id = w.assignee_id
               where w.assignee_id in (%s) and w.is_done = 0
               order by w.start_date ASC
            ''' % people_id_string)
    assignments = {}
    for w in work_data:
        items = assignments.get(w['assignee_name'], [])
        items.append({
            'work_id': w['id'],
            'label': w['title'],
            'project_id': w['project_id'],
            'assignee_name': w['assignee_name'],
            'project_name': w['project_name'],
            'effort_left_d': w['effort_left_d'],
            'key_date': dovetail.util.condition_date(w['work_key_date']),
            'start_date': dovetail.util.condition_date(w['start_date']),
            'end_date': dovetail.util.condition_date(w['end_date'])
        })
        assignments[w['assignee_name']] = items

    return assignments

def select_key_work_for_project(connection, project_id):
    work_data = connection.execute(
            '''select id, title, effort_left_d, prereqs, assignee_id, key_date
               from work
               where project_id = %d AND key_date NOT NULL AND work.is_done = 0
               order by key_date ASC
            ''' % int(project_id))
    result = [fields_to_work_object(w) for w in work_data]
    return result

def select_done_work_for_project(connection, project_id):
    work_data = connection.execute(
            '''select w.id, w.title, w.start_date, w.end_date,
               people.id as person_id, people.name as assignee_name,
               people.picture as assignee_picture, w.effort_left_d, w.key_date, w.prereqs
               from work as w
               inner join people on people.id = w.assignee_id
               where w.project_id = %d and w.is_done = 1
               order by topo_order ASC
            ''' % int(project_id))

    result = work_data_to_work_object(work_data)
    return result

def update_work(connection, work_data):
    statement = database.work.update().\
        where(database.work.c.id == work_data['id']).\
        values(work_data['fields'])
    connection.execute(statement)
    return

def update_work_dates(connection, work_collection):
    for w in work_collection:
        statement = database.work.update().\
            where(database.work.c.id == w.work_id).\
            values({'start_date': w.est_start_date(), 'end_date': w.est_end_date()})
        connection.execute(statement)
    return

def update_work_topo_order(connection, work_collection):
    for i, w in enumerate(work_collection):
        statement = database.work.update().\
            where(database.work.c.id == w.work_id).\
            values({'topo_order': i})
        connection.execute(statement)
    return

def mark_work_done(connection, work_ids):
    for w in work_ids:
        statement = database.work.update().\
            where(database.work.c.id == w).\
            values({'is_done': True})
        connection.execute(statement)
    return

def mark_work_undone(connection, work_ids):
    for w in work_ids:
        statement = database.work.update().\
            where(database.work.c.id == w).\
            values({'is_done': False})
        connection.execute(statement)
    return
