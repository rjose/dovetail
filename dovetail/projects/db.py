import json
import dovetail.database as database
import dovetail.work.models as work
import dovetail.people.db as people_db

def select_project_collection(connection):
    data = connection.execute(database.projects.select())
    result = [{
            'project_id': row['id'],
            'title': row['name'],
            'target_date': database.format_date(row['target_date']),
            'est_date': database.format_date(row['est_end_date']),
            'detail_url': '/projects/%d' % row['id'],
            'key_dates': work.get_key_work_for_project(connection, row['id'])
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
        'work': work.get_work_for_project(connection, project_id)
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
