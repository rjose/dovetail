import json
import dovetail.util
import dovetail.database as database
import dovetail.work.db as work_db
import dovetail.people.db as people_db

from dovetail.projects.project import Project
from dovetail.work.work import Work

# This adds 'key_work' to each project as well
def select_project_collection(connection):
    data = connection.execute(database.projects.select())
    result = []
    for row in data:
        p = Project(row['id'])
        p.name = row['name']
        p.target_date = row['target_date']
        p.est_end_date = row['est_end_date']
        p.key_work = work_db.select_key_work_for_project(connection, row['id'])
        result.append(p)
    return result


def select_project(connection, project_id):
    result = Project(project_id)
    data = connection.execute(database.projects.select(
        database.projects.c.id == project_id)).first()

    result.name = data['name']
    result.target_date = dovetail.util.format_date(data['target_date'])
    result.est_end_date = dovetail.util.format_date(data['est_end_date'])
    result.participants = people_db.select_project_participants(connection, project_id)
    result.work = work_db.select_work_for_project(connection, project_id)
    return result

def insert_project(connection, name, target_date):
    connection.execute(database.projects.insert(),
           name = name,
           target_date = target_date)
    return

def add_project_participant(connection, project_id, person_id):
    data = connection.execute('''
        select project_id, person_id from project_participants
        where project_id = %d and
              person_id = %d
        ''' % (int(project_id), int(person_id)))

    if data.first():
        return

    connection.execute(database.project_participants.insert(),
           project_id = project_id,
           person_id = person_id)
    return

def update_project_and_work_dates(connection, projects):
    for p in projects:
        statement = database.projects.update().\
            where(database.projects.c.id == p.project_id).\
            values({'est_end_date': p.est_end_date})
        connection.execute(statement)
        work_db.update_work_dates(connection, p.work)
    return

def select_all_project_ids(connection):
    data = connection.execute('select id from projects order by value desc')
    result = [row['id'] for row in data]
    return result

def get_projects_for_scheduling(connection):
    project_ids = select_all_project_ids(connection)
    projects = [Project(project_id) for project_id in project_ids]
    for p in projects:
        work_data = work_db.select_work_for_project2(connection, p.project_id)
        p.work = [Work(
            w['id'],
            w['title'],
            w['effort_left_d'],
            w['prereqs'],
            w['assignee']['id'],
            w['key_date']) for w in work_data]
    return projects

