class Work():
    
    def __init__(self, work_id):
        self.work_id = work_id
        self.title = ''
        self.effort_left_d = 0
        self.prereqs = []
        self.assignee_id = None
        self.key_date = None
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

    def earliest_start_date(self, work_dict, cur_day):
        result = cur_day
        for work_id in self.prereqs:
            end_date = work_dict[work_id].est_end_date()
            if end_date and end_date > result:
                result = end_date
        return result

