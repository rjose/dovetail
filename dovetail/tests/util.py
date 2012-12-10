from datetime import datetime
from dovetail.work.work import Work

nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y") # Thu
nov2 = datetime.strptime("Nov 2, 2012", "%b %d, %Y")
nov3 = datetime.strptime("Nov 3, 2012", "%b %d, %Y") # Sat
nov4 = datetime.strptime("Nov 4, 2012", "%b %d, %Y") # Sun
nov5 = datetime.strptime("Nov 5, 2012", "%b %d, %Y") # Mon
nov6 = datetime.strptime("Nov 6, 2012", "%b %d, %Y")
nov7 = datetime.strptime("Nov 7, 2012", "%b %d, %Y") # Wed
nov8 = datetime.strptime("Nov 8, 2012", "%b %d, %Y") # Thu
nov9 = datetime.strptime("Nov 9, 2012", "%b %d, %Y") # Fri
nov12 = datetime.strptime("Nov 12, 2012", "%b %d, %Y") # Fri
nov15 = datetime.strptime("Nov 15, 2012", "%b %d, %Y")
nov19 = datetime.strptime("Nov 19, 2012", "%b %d, %Y")
nov23 = datetime.strptime("Nov 23, 2012", "%b %d, %Y")

def construct_work(id, title, effort_left_d, prereqs, assignee_id, key_date):
    result = Work(id)
    result.title = title
    result.effort_left_d = effort_left_d
    result.prereqs = prereqs
    result.assignee_id = assignee_id
    result.key_date = key_date
    return result

