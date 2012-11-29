from datetime import datetime

def standardize_date(date):
    result = datetime(date.year, date.month, date.day)
    return result

def parse_date(date_string):
    return datetime.strptime(date_string, "%b %d, %Y")

def condition_date(d):
    if d:
        return datetime.strptime(d, '%Y-%m-%d')
    else:
        return d

def format_effort_left(effort_left_d):
    if effort_left_d:
        return '%.2f d' % effort_left_d
    else:
        return '0.1 d'

