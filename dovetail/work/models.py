def get_work_for_project(connection, project_id):
    # TODO: Order by priority (from algo)
    work_data = connection.execute(
            '''select w.id, w.title, people.name as assignee, people.picture as picture,
               w.effort_left_d, w.key_date, w.prereqs
               from work as w
               inner join people on people.id = w.assignee_id
               where w.project_id = %d
            ''' % int(project_id))
    result = [{
              'id': w['id'], 
              'title': w['title'],
              'assignee': {'name': w['assignee'], 'picture': w['picture']},
              'effort_left_d': w['effort_left_d'], 
              'key_date': w['key_date'],
              'prereqs': w['prereqs']
              } 
             for w in work_data]
    return result

def format_effort_left(effort_left_d):
    if effort_left_d:
        return '%.2fd' % effort_left_d
    else:
        return '0.1d'

