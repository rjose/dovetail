from datetime import datetime
from dovetail.timeline.timeline import Timeline
import dovetail.projects.db as projects_db

class Scheduler:

    def __init__(self, cur_date):
        self.timelines = {}
        self.work_dict = {}
        self.cur_date = cur_date
        return

    def get_assignee_timeline(self, person_id):
        if self.timelines.has_key(person_id):
            result = self.timelines[person_id]
        else:
            # TODO: Figure out how to handle user-specific nonworkdays
            result = Timeline(self.cur_date)
            self.timelines[person_id] = result
        return result

    def schedule_work(self, work):
        timeline = self.get_assignee_timeline(work.assignee_id)
        if work.key_date:
            slot = timeline.schedule_at_end_date(work.key_date, work.effort_left_d)
        else:
            start_date = work.earliest_start_date(self.work_dict, self.cur_date)
            slot = timeline.schedule_at_start_date(start_date, work.effort_left_d)

        work.schedule(slot)
        return


    def schedule_projects(self, projects):
        for p in projects:
            est_project_end = self.cur_date
            for w in p.work:
                self.work_dict[w.work_id] = w
                self.schedule_work(w)
                w_end_date = w.est_end_date()
                if w_end_date > est_project_end:
                    est_project_end = w_end_date
            p.est_end_date = est_project_end
        return projects


def reschedule_world(connection):
    scheduler = Scheduler(datetime.now())
    projects = projects_db.get_projects_for_scheduling(connection)
    projects = scheduler.schedule_projects(projects)
    projects_db.update_project_and_work_dates(connection, projects)
    return
