from dovetail.timeline.timeline import Timeline
from dovetail.work.work import earliest_start_date

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
            pass
        else:
            # TODO: Make this into a single function call
            start_date = earliest_start_date(work, self.work_dict, self.cur_date)
            day = timeline.day_from_date(start_date)
            slot, parent_index = timeline.find_slot(day, work.effort_left_d)
            slot = timeline.claim_slot(slot, parent_index)
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
