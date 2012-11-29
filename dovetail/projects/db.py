import json
import dovetail.database as database
import dovetail.work.db as work_db
import dovetail.people.db as people_db

def select_project_collection(connection):
    data = connection.execute(database.projects.select())
    result = [{
            'project_id': row['id'],
            'title': row['name'],
            'target_date': database.format_date(row['target_date']),
            'est_date': database.format_date(row['est_end_date']),
            'detail_url': '/projects/%d' % row['id'],
            'key_dates': work_db.select_key_work_for_project(connection, row['id'])
            } for row in data]
    return result


def select_project(connection, project_id):
    # TODO: Use a single query to get the project participants as well
    data = connection.execute(database.projects.select(
        database.projects.c.id == project_id)).first()

    result = {
        'project_id': data['id'],
        'name': data['name'],
        'stats': {
            'target_date': database.format_date(data['target_date']),
            'est_date': database.format_date(data['est_end_date']),
            'total_effort': 'TODO',
            },
        'participants': people_db.select_project_participants(connection, project_id),
        'work': work_db.select_work_for_project(connection, project_id)
        }
    return result

def insert_project(connection, name, target_date):
    connection.execute(database.projects.insert(),
           name = name,
           target_date = target_date)
    return

def add_project_participant(connection, project_id, person_id):
    # TODO: Handle case where participant is already part of the project
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
