from dovetail.work.work import Work

def construct_work(id, title, effort_left_d, prereqs, assignee_id, key_date):
    result = Work(id)
    result.title = title
    result.effort_left_d = effort_left_d
    result.prereqs = prereqs
    result.assignee_id = assignee_id
    result.key_date = key_date
    return result

