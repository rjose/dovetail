import json

# TODO: Get rid of this import
import dovetail.work.db as work_db
import dovetail.database as database
import dovetail.people.db as people_db

def shorten_name(name):
    return name

def format_prereqs(prereqs):
    if prereqs:
        return prereqs
    else:
        return "[]"


def project_work_to_string(work_data):
    # TODO: Delete this example data
    # work_data = "[240, 'BB', '0.1d', 'A prerequisite', [], 'Dec 20, 2012']\n"
    # work_data += "[320, 'RJ', '1d', 'Another prerequisite', [], '']\n"
    # work_data += "[121, 'RJ', '2.5d', 'Figure out thing for thing', [240, 320], '']\n"
    result = ''
    for w in work_data:
        result += '[%d, "%s", "%s", "%s", %s, "%s"]\n' % (
                w['id'],
                shorten_name(w['assignee']['name']),
                work_db.format_effort_left(w['effort_left_d']),
                w['title'],
                format_prereqs(w['prereqs']),
                database.format_date(w['key_date']))
    return result

def parse_workline(connection, workline):
    data = json.loads(workline)
    # TODO: Do some error handling here
    person = people_db.select_person_by_name(connection, data[1])
    effort_left_d = float(data[2].split()[0])
    key_date = None
    if data[5] != '?':
        key_date = dovetail.util.parse_date(data[5])

    result = {
            'id': data[0],
            'fields': {
                'assignee_id': person['id'],
                'effort_left_d': effort_left_d,
                'title': data[3],
                'prereqs': str(data[4]),
                'key_date': key_date
                }
            }
    return result


