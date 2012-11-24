import dovetail.database as database

def get_projects_data(connection):
    data = connection.execute(database.projects.select())
    result = []
    for row in data:
        p = {
                'project_id': row['id'],
                'title': row['name'],
                'target_date': database.format_date(row['target_date']),
                'est_date': database.format_date(row['est_date']),
                'detail_url': '/projects/%d' % row['id'],
                'key_dates': []
            }
        result.append(p)
    return result + get_phony_project_data()

# TODO: Delete this
def get_phony_project_data():
    search_project = {'project_id': 1,
        'title': 'Search',
        'target_date': 'Feb 15, 2012',
        'est_date': 'Feb 10, 2012',
        'detail_url': '/projects/1',
        'key_dates': [['Integration with PAL', 'Dec 15, 2012']]}
    endorsements_project = {'project_id': 2,
        'title': 'Endorsements',
        'target_date': 'Mar 15, 2012',
        'est_date': 'Mar 20, 2012',
        'detail_url': '/projects/2',
        'key_dates': []}
    rich_media_project = {'project_id': 3,
        'title': 'Rich Media',
        'target_date': 'Mar 15, 2012',
        'est_date': 'Mar 2, 2012',
        'detail_url': '/projects/3',
        'key_dates': []}
    mentions_project = {'project_id': 4,
        'title': 'Mentions',
        'target_date': 'Mar 25, 2012',
        'est_date': 'Mar 25, 2012',
        'detail_url': '/projects/4',
        'key_dates': []}
    return [search_project, endorsements_project, rich_media_project, mentions_project]

def get_project_details(connection, project_id):
    # TODO: Order by priority (from algo)
    work_data = connection.execute(
            '''select w.id, w.title, people.name as assignee, people.picture as picture,
               w.effort_left_d, w.key_date, w.prereqs
               from work as w
               inner join people on people.id = w.assignee_id
               where w.project_id = %d
            ''' % int(project_id))
    work = [{'id': w['id'], 'title': w['title'],
        'assignee': {'name': w['assignee'], 'picture': w['picture']},
        'effort_left_d': w['effort_left_d'], 'key_date': w['key_date'],
        'prereqs': w['prereqs']} for w in work_data]

    particpants_data = connection.execute(
            '''select id, name, title, team, picture from people
               inner join project_participants on project_participants.person_id = people.id
               where project_participants.project_id= %d
               order by name''' % int(project_id))
    participants = [{'id': p['id'], 'name': p['name'], 'title': p['title'],
        'team': p['team'], 'picture': p['picture']}
            for p in particpants_data]
    data = connection.execute(database.projects.select(
        database.projects.c.id == project_id)).first()
    result = {
        'project_id': data['id'],
        'name': data['name'],
        'stats': {
            'target_date': database.format_date(data['target_date']),
            'est_date': database.format_date(data['est_date']),
            'total_effort': 'TODO',
            },
        'participants': participants,
        'work': work
        }

    return result

def get_phony_project_details(project_id):
    rino = {'name': 'Rino Jose',
            'picture': 'https://m1-s.licdn.com/mpr/mpr/shrink_80_80/p/2/000/019/20e/2464c31.jpg'}
    result = {
        'project_id': 2,
        'name': 'Endorsements',
        'stats': {
            'target_date': 'Mar 15, 2012',
            'est_date': 'Mar 20, 2012',
            'total_effort': '40 man-days',
            },
        'participants': [
            {'name': 'Rino Jose', 'title': "Engineering Manager", 'team': 'Mobile'}
            ],
        'work': [
            {'name': 'Figure out the thing for the thing', 'is_done': 'Done: Oct 14, 2012',
                'assignee': rino},
            {'name': 'Do the actual work', 'assignee': rino},
            {'name': 'Do more work', 'key_date': 'Dec 19, 2012', 'assignee': rino},
            ]
        }
    return result
