import dovetail.database as database
import dovetail.work.models as work
import dovetail.people.models as people

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
        'participants': people.get_participants_for_project(connection, project_id),
        'work': work.get_work_for_project(connection, project_id)
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

def format_prereqs(prereqs):
    if prereqs:
        return prereqs
    else:
        return "[]"

# TODO: TDD this
def shorten_name(name):
    return name

