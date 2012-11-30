import dovetail.database as database
from dovetail.people.person import Person

def select_project_participants(connection, project_id):
    particpants_data = connection.execute(
            '''select id, name, title, team, picture from people
               inner join project_participants on project_participants.person_id = people.id
               where project_participants.project_id= %d
               order by name''' % int(project_id))
    result = [{'id': p['id'], 'name': p['name'], 'title': p['title'],
        'team': p['team'], 'picture': p['picture']}
            for p in particpants_data]
    return result

def select_person_by_name(connection, name):
    person_data = connection.execute(database.people.select(
        database.people.c.name == name)).first()
    result = Person(person_data['id'])
    result.name = person_data['name']
    result.picture = person_data['picture']
    result.team = person_data['team']
    result.title = person_data['title']
    return result
