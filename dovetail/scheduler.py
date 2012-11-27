from dovetail.timeline.timeline import Timeline

class Scheduler:

    def __init__(self, cur_date):
        self.timelines = {}
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
