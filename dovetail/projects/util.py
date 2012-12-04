import json

# TODO: Get rid of this import
import dovetail.work.db as work_db
import dovetail.database as database
import dovetail.people.db as people_db
import dovetail.util

def shorten_name(name):
    return name

def format_prereqs(prereqs):
    if prereqs:
        return prereqs
    else:
        return "[]"


def project_work_to_string(work_data):
    result = ''
    for w in work_data:
        result += '[%d, "%s", "%s", "%s", %s, "%s"]\n' % (
                w.work_id,
                shorten_name(w.assignee.name),
                dovetail.util.format_effort_left(w.effort_left_d),
                w.title,
                format_prereqs(w.prereqs),
                dovetail.util.format_date(w.key_date))
    return result

def parse_workline(connection, workline):
    data = json.loads(workline)
    # TODO: Do some error handling here
    person = people_db.select_person_by_name(connection, data[1])
    effort_left_d = float(data[2].split()[0])
    key_date = None
    if data[5] not in ['?', '']:
        key_date = dovetail.util.parse_date(data[5])

    result = {
            'id': data[0],
            'fields': {
                'assignee_id': person.person_id,
                'effort_left_d': effort_left_d,
                'title': data[3],
                'prereqs': str(data[4]),
                'key_date': key_date
                }
            }
    return result

def compute_status(target_date, est_date):
    delta = est_date - target_date
    if (delta.days <= -5):
        result = {'label': 'EARLY', 'class': 'label-success', 'date_class': ''}
    elif (delta.days > -5 and delta.days <= 0):
        result = {'label': 'ON TRACK', 'class': '', 'date_class': ''}
    else:
        result = {'label': 'LATE', 'class': 'label-important', 'date_class': 'text-error'}
    return result


