from flask import (Blueprint, Response, json, render_template, request,
        redirect, url_for, g)
from datetime import datetime

import dovetail.database as database
import dovetail.projects.db as projects_db
import dovetail.people.db as people_db
import dovetail.work.db as work_db
import dovetail.scheduler

mod = Blueprint('work', __name__)

@mod.route('/api/work', methods=['POST'])
def api_work():
    # Condition data from request
    title = request.values['title']
    assignee_id = int(request.values['assignee_id'])
    effort_left_d = float(request.values['effort_left_d'])
    project_id = int(request.values['project_id'])

    insert_result = g.connection.execute(database.work.insert(),
           title = title,
           assignee_id = assignee_id,
           project_id = project_id,
           effort_left_d = effort_left_d)

    response_data = {'work_id': insert_result.inserted_primary_key}
    dovetail.scheduler.reschedule_world(g.connection)
    return Response(json.dumps(response_data), status=200, mimetype='application/json')

@mod.route('/api/work/<int:work_id>/mark_undone', methods=['POST'])
def api_mark_work_undone(work_id):
    work_db.mark_work_undone(g.connection, [work_id])
    response_data = {}
    result = Response(json.dumps(response_data), status=200, mimetype='application/json')
    return result
