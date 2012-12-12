from datetime import datetime, timedelta
import dovetail.util
from dovetail.charts.support.gantt import Gantt


class ProjectCollectionTimelineChart:
    def __init__(self, cur_day, projects):
        self.cur_day = dovetail.util.standardize_date(cur_day)
        self.data = []

        if not projects:
            return

        for p in projects:
            row = {
                'label': p.name,
                'bars': [self.project_to_bar(p)]
            }
            self.data.append(row)
            pass
        return

    def project_to_bar(self, project):
        result = {
            'id': project.project_id,
            'start': project.est_start_date,
            'end': project.est_end_date,
            'effort_d': project.total_effort(),
            'color': self.get_project_color(project)
        }
        return result

    def as_json(self):
        max_date = self.cur_day + timedelta(21)
        gantt = Gantt(self.cur_day, self.data, max_date)
        return gantt.as_json()

    def get_project_color(self, project):
        if not project.est_end_date:
            return '#000'

        delta = project.est_end_date - project.target_date
        if (delta.days <= -5):
            color = '#468847' # Green
        elif (delta.days > -5 and delta.days <= 0):
            color = '#999' # Gray
        else:
            color = '#B94A48' # Red
        return color

