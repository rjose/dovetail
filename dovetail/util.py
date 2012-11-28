from datetime import datetime

def parse_date(date_string):
    return datetime.strptime(date_string, "%b %d, %Y")

def condition_date(d):
    if d:
        return datetime.strptime(d, '%Y-%m-%d')
    else:
        return d


