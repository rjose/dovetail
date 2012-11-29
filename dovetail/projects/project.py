import dovetail.projects.db as project_db
import dovetail.work.db as work_db
from dovetail.work.work import Work
from pygraph.classes.digraph import digraph
from pygraph.algorithms.sorting import topological_sorting

def get_projects_for_scheduling(connection):
    project_ids = project_db.select_all_project_ids(connection)
    projects = [Project(project_id) for project_id in project_ids]
    for p in projects:
        work_data = work_db.select_work_for_project2(connection, p.project_id)
        p.work = [Work(w['id'], w['title'], w['effort_left_d'], w['prereqs'],
            w['assignee']['id'], w['key_date']) for w in work_data]
    return projects

class Project:

    def __init__(self, project_id):
        self.project_id = project_id
        self.work = []
        self.est_end_date = None

    def topo_sort_work(self):
        # Reverse work to preserver initial order among items of same rank
        my_work = self.work

        work_dict = {}
        for w in my_work:
            work_dict[w.work_id] = w

        graph = digraph()
        graph.add_nodes(my_work)

        for w in my_work:
            for p in w.prereqs:
                graph.add_edge((work_dict[p], w))
        self.work = topological_sorting(graph)
        return
