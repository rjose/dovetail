import dovetail.util

class TimelineRenderer():
    def __init__(self, cur_day, timeline_data, highlighted_project_id=None):
        self.cur_day = dovetail.util.standardize_date(cur_day)
        self.timelines = timeline_data
        self.highlighted_project_id = highlighted_project_id

        # Timeline view params
        self.Y_STEP = 30
        self.START_X = 50
        self.START_Y = 20
        self.BAR_HEIGHT = 25
        self.PIXELS_PER_DAY = 20
        return

    def date_to_x(self, date):
        delta = date - self.cur_day
        result = delta.days * self.PIXELS_PER_DAY
        return result

    # TODO: Rework this so it converts into JSON data
    def get_timeline_code(self):
        timeline_rows = self.get_timeline_rows()
        result = self.render_timeline_rows(timeline_rows)
        return result

    def construct_bars(self, work_data):
        bars = []
        for work in work_data:
            x_start = self.date_to_x(work['start_date'])
            x_end = self.date_to_x(work['end_date'])
            if x_start == x_end:
                x_end = x_start + work['effort_left_d']*self.PIXELS_PER_DAY
            x_end -= 2
            color = 'blue'
            if self.highlighted_project_id:
                if self.highlighted_project_id == work['project_id']:
                    color = 'blue'
                else:
                    color = 'gray'

            bar = {
                'label': work['label'],
                'x_start': x_start,
                'x_end': x_end,
                'width': x_end - x_start,
                'color': color
            }
            bars.append(bar)
        return bars
        
    # TODO: Rename this
    def get_timeline_rows(self):
        names = self.timelines.keys()
        names.sort()

        cur_y = self.START_Y
        result = []
        for name in names:
            row = {
                'label': name,
                'y': cur_y
            }
            row['bars'] = self.construct_bars(self.timelines[name])
            result.append(row)
            cur_y += self.Y_STEP

        return result

    def render_timeline_rows(self, rows):
        # TODO: Render data into the page and have javascript take care of it
        rendered_rows = []
        for row in rows:
            for bar in row['bars']:
                rendered_rows.append('Planman.addRectangle(%.1f, %.1f, %.1f, %1.f, "%s");'
                        % (bar['x_start'], row['y'], bar['width'], self.BAR_HEIGHT, bar['color']))
        result = '\n'.join(rendered_rows)
        return result

