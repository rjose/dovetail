from datetime import datetime, timedelta
import dovetail.util
import json

class Gantt:
    # Each row looks like this:
    # [{label: 'Person', bars: [{start: Date, end: Date, effort_d: Float, color: 'blue'}]}
    def __init__(self, cur_day, rows, max_date):
        # Chart params
        self.Y_STEP = 30
        self.START_X = 100
        self.START_Y = 20
        self.BAR_HEIGHT = 25
        self.PIXELS_PER_DAY = 30
        self.X_MARGIN = 2

        self.cur_day = dovetail.util.standardize_date(cur_day)
        self.max_date = dovetail.util.standardize_date(max_date)
        self.tick_dates = self.compute_tick_dates(self.cur_day, self.max_date)
        self.data = self.transform(rows)
        return

    def date_to_x(self, date):
        delta = date - self.cur_day
        result = self.START_X + delta.days * self.PIXELS_PER_DAY
        return result

    def compute_tick_dates(self, start_day, max_day):
        one_day = timedelta(1)
        one_week = timedelta(7)

        result = []
        # Find next monday
        cur_day = start_day
        while cur_day.weekday() != 0: # Not monday
            cur_day = cur_day + one_day

        result.append(cur_day)

        # Add mondays up till the max_day
        cur_day = cur_day + one_week
        while cur_day <= max_day:
            result.append(cur_day)
            cur_day = cur_day + one_week

        return result

    def date_labels(self):
        return self.data['dates']

    def transform_row(self, row, cur_y):
        result = {
            'label': row['label'],
            'y': cur_y,
            'bars': []
        }

        for b in row['bars']:
            # Figure out start and ending x values for each bar
            x_start = self.date_to_x(b['start'])
            x_end = self.date_to_x(b['end'])
            if x_start == x_end:
                x_end = x_start + b['effort_d'] * self.PIXELS_PER_DAY
            x_end -= self.X_MARGIN

            result['bars'].append({
                'x': x_start,
                'width': x_end - x_start,
                'height': self.BAR_HEIGHT,
                'color': b['color']
            })
        return result

    def transform(self, rows):
        result = {
            'rows': [],
            'dates': []
        }

        cur_y = self.START_Y
        for r in rows:
            result['rows'].append(self.transform_row(r, cur_y))
            cur_y += self.Y_STEP

        result['dates'] = [{
            'label': dovetail.util.format_date(d),
            'x': self.date_to_x(d)} for d in self.tick_dates]
        return result

    def as_json(self):
        return json.dumps(self.data)

