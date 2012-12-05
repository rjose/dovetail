import dovetail.database as database
from dovetail.people.person import Person

def select_people(connection):
    people_data = connection.execute('select id, name from people order by name')
    result = []
    for d in people_data:
        p = Person(d['id'])
        p.name = d['name']
        result.append(p)
    return result

def select_project_participants(connection, project_id):
    particpants_data = connection.execute(
            '''select id, name, title, team, picture from people
               inner join project_participants on project_participants.person_id = people.id
               where project_participants.project_id= %d
               order by name''' % int(project_id))
    result = []
    for d in particpants_data:
        p = Person(d['id'])
        p.name = d['name']
        p.title = d['title']
        p.team = d['team']
        p.picture = d['picture']
        result.append(p)
    return result

def data_to_person(data):
    result = Person(data['id'])
    result.name = data['name']
    result.picture = data['picture']
    result.team = data['team']
    result.title = data['title']
    return result

def select_person(connection, person_id):
    person_data = connection.execute(database.people.select(
        database.people.c.id == person_id)).first()
    result = data_to_person(person_data)
    return result

def select_person_by_name(connection, name):
    person_data = connection.execute(database.people.select(
        database.people.c.name == name)).first()
    result = data_to_person(person_data)
    return result
