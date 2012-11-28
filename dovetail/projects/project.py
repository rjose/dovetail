import dovetail.projects.db as project_db
import dovetail.work.db as work_db
from dovetail.work.work import Work

def get_projects_for_scheduling(connection):
    project_ids = project_db.select_all_project_ids(connection)
    projects = [Project(project_id) for project_id in project_ids]
    for p in projects:
        work_data = work_db.select_work_for_project2(connection, p.project_id)
        p.work = [Work(w['id'], w['title'], w['effort_left_d'], w['prereqs'],
            w['assignee']['id'], w['key_date']) for w in work_data]
    return projects

class Project:

    def __init__(self, project_id):
        self.project_id = project_id
        self.work = []
        self.est_end_date = None
