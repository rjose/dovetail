from datetime import datetime, timedelta
import dovetail.util
from dovetail.charts.support.gantt import Gantt

class PersonTimelineChart:
    def __init__(self, cur_day, person):
        self.cur_day = dovetail.util.standardize_date(cur_day)
        self.data = [{
            'label': person.name,
            'bars': self.work_to_bars(person.work)
        }]
        return

    def work_to_bars(self, work):
        colors = ['#08C', '#1531AE', '#FF8300', '#024E68', '#2D3C82', '#A65500', '#2D3C82']
        project_color = {}

        result = []
        color = '#08C'
        for w in work:
            result.append({
                'id': w.work_id,
                'start': w.start_date,
                'end': w.end_date,
                'effort_d': w.effort_left_d,
                'color': self.get_project_color(w.project_id, project_color, colors)
            })
        return result

    def get_project_color(self, project_id, project_color_dict, colors):
        if not project_color_dict.has_key(project_id):
            new_color_index = len(project_color_dict) % len(colors)
            project_color_dict[project_id] = new_color_index

        result = colors[project_color_dict[project_id]]
        return result

    def as_json(self):
        # Set the end date of the chart to be 3 weeks out
        max_date = self.cur_day + timedelta(21)
        gantt = Gantt(self.cur_day, self.data, max_date)
        return gantt.as_json()
