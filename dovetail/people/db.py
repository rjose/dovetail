import dovetail.database as database
from dovetail.people.person import Person

def fields_to_person_object(fields):
    result = Person(fields['id'])

    for f in fields.keys():
        if f == 'name':
            result.name = fields[f]
        elif f == 'title':
            result.title = fields[f]
        elif f == 'team':
            result.team = fields[f]
        elif f == 'picture':
            result.picture = fields[f]
    return result

def select_people(connection):
    people_data = connection.execute('select id, name from people order by name')
    result = [fields_to_person_object(d) for d in people_data]
    return result

def select_project_participants(connection, project_id):
    particpants_data = connection.execute(
            '''select id, name, title, team, picture from people
               inner join project_participants on project_participants.person_id = people.id
               where project_participants.project_id= %d
               order by name''' % int(project_id))
    result = [fields_to_person_object(d) for d in particpants_data]
    return result

def select_person(connection, person_id):
    person_data = connection.execute(database.people.select(
        database.people.c.id == person_id)).first()
    result = fields_to_person_object(person_data)
    return result

def select_person_by_name(connection, name):
    person_data = connection.execute(database.people.select(
        database.people.c.name == name)).first()
    result = fields_to_person_object(person_data)
    return result
