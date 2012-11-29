import dovetail.database as database
from datetime import datetime
import json
import dovetail.util

def select_work_for_project(connection, project_id):
    # TODO: Order by priority (from algo)
    work_data = connection.execute(
            '''select w.id, w.title,
               people.id as person_id, people.name as assignee, people.picture as picture,
               w.effort_left_d, w.key_date, w.prereqs
               from work as w
               inner join people on people.id = w.assignee_id
               where w.project_id = %d
            ''' % int(project_id))
    result = [{
              'id': w['id'], 
              'title': w['title'],
              'assignee': {'id': w['person_id'], 'name': w['assignee'], 'picture': w['picture']},
              'effort_left_d': w['effort_left_d'], 
              'key_date': dovetail.util.condition_date(w['key_date']),
              'prereqs': w['prereqs']
              } 
             for w in work_data]
    return result

def select_work_for_project2(connection, project_id):
    # TODO: Order by priority (from algo)
    work_data = connection.execute(
            '''select w.id, w.title,
               people.id as person_id, people.name as assignee, people.picture as picture,
               w.effort_left_d, w.key_date, w.prereqs
               from work as w
               inner join people on people.id = w.assignee_id
               where w.project_id = %d
            ''' % int(project_id))
    result = [{
              'id': w['id'],
              'title': w['title'],
              'assignee': {'id': w['person_id'], 'name': w['assignee'], 'picture': w['picture']},
              'effort_left_d': w['effort_left_d'],
              'key_date': dovetail.util.condition_date(w['key_date']),
              'prereqs': json.loads(w['prereqs'])
              }
             for w in work_data]
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
