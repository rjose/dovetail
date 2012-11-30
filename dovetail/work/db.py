from datetime import datetime
import json
import dovetail.util
import dovetail.database as database
from dovetail.work.work import Work
from dovetail.people.person import Person

# This augments work with an assignee Person object
def select_work_for_project(connection, project_id):
    work_data = connection.execute(
            '''select w.id, w.title,
               people.id as person_id, people.name as assignee_name,
               people.picture as assignee_picture, w.effort_left_d, w.key_date, w.prereqs
               from work as w
               inner join people on people.id = w.assignee_id
               where w.project_id = %d
               order by topo_order ASC
            ''' % int(project_id))

    result = []
    for w in work_data:
        work = Work(w['id'],
                    w['title'],
                    w['effort_left_d'],
                    dovetail.util.condition_prereqs(w['prereqs']),
                    w['person_id'],
                    dovetail.util.condition_date(w['key_date']))

        assignee = Person(w['person_id'])
        assignee.name = w['assignee_name']
        assignee.picture = w['assignee_picture']
        work.assignee = assignee
        result.append(work)
    return result


def select_key_work_for_project(connection, project_id):
    work_data = connection.execute(
            '''select id, title, key_date
               from work
               where project_id = %d AND key_date NOT NULL
               order by key_date ASC
            ''' % int(project_id))
    return [[w['title'], dovetail.util.condition_date(w['key_date'])] for w in work_data]

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
