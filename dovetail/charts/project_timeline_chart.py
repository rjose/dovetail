from datetime import datetime, timedelta
import dovetail.util
from dovetail.charts.support.gantt import Gantt

class ProjectTimelineChart:
    def __init__(self, project_id, cur_day, timelines):
        self.cur_day = dovetail.util.standardize_date(cur_day)
        self.project_id = project_id
        self.data = []

        if not timelines:
            return

        names = timelines.keys()
        names.sort()

        for name in names:
            work = timelines[name]
            row = {
                'label': name,
                'bars': self.work_to_bars(work)
            }
            self.data.append(row)
        return

    def work_to_bars(self, work):
        result = []
        for w in work:
            if w['project_id'] == self.project_id:
                color = '#08C'
            else:
                color = 'gray'
            result.append({
                'id': w['work_id'],
                'start': w['start_date'],
                'end': w['end_date'],
                'effort_d': w['effort_left_d'],
                'color': color
            })
        return result

    def as_json(self):
        # Set the end date of the chart to be 3 weeks out
        max_date = self.cur_day + timedelta(21)
        gantt = Gantt(self.cur_day, self.data, max_date)
        return gantt.as_json()
