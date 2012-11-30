from pygraph.classes.digraph import digraph
from pygraph.algorithms.sorting import topological_sorting

class Project:

    def __init__(self, project_id):
        self.project_id = project_id
        self.work = []
        self.name = None
        self.participants = []
        self.target_date = None
        self.est_end_date = None
        return

    def total_effort(self):
        return reduce(lambda x, y: x + y, [w.effort_left_d for w in self.work], 0)

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
