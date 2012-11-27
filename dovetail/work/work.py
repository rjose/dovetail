def earliest_start_date(work, work_dict, cur_day):
    result = cur_day
    for work_id in work.prereqs:
        end_date = work_dict[work_id].est_end_date()
        if end_date and end_date > result:
            result = end_date
    return result

class Work():
    
    def __init__(self, work_id, title, effort_left_d, prereqs, assignee_id, key_date):
        self.work_id = work_id
        self.title = title
        self.effort_left_d = effort_left_d
        self.prereqs = prereqs
        self.assignee_id = assignee_id
        self.key_date = key_date
        self.slot = None

    def schedule(self, slot):
        self.slot = slot

    def est_start_date(self):
        if self.slot:
            return self.slot.start_date
        else:
            return None

    def est_end_date(self):
        if self.slot:
            return self.slot.end_date
        else:
            return None
