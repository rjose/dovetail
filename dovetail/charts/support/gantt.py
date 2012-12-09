import dovetail.util
import json

class Gantt:
    # Each row looks like this:
    # [{label: 'Person', bars: [{start: Date, end: Date, effort_d: Float, color: 'blue'}]}
    def __init__(self, cur_day, rows):
        # Chart params
        self.Y_STEP = 30
        self.START_X = 100
        self.START_Y = 20
        self.BAR_HEIGHT = 25
        self.PIXELS_PER_DAY = 20
        self.X_MARGIN = 2

        self.cur_day = dovetail.util.standardize_date(cur_day)
        self.data = self.transform(rows)
        return

    def date_to_x(self, date):
        delta = date - self.cur_day
        result = self.START_X + delta.days * self.PIXELS_PER_DAY
        return result

    def transform_row(self, row, cur_y):
        result = {
            'label': row['label'],
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
                'y': cur_y,
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

        # TODO: Add date labels
        return result

    def as_json(self):
        return json.dumps(self.data)

