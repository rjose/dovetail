import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.projects.project import Project
from dovetail.work.work import Work
from dovetail.tests.util import construct_work

class TestProject(unittest.TestCase):

    def test_sort_work(self):
        # Assignees
        person_id1 = 101
        person_id2 = 102
        person_id3 = 103

        # Projects
        p1 = Project(1)
        p1_w1 = construct_work(1, "p1 w1", 1.0, [6], person_id1, None)
        p1_w2 = construct_work(2, "p1 w2", 1.0, [], person_id1, None)
        p1_w3 = construct_work(5, "p1 w3", 0.1, [2, 1], person_id1, None)
        p1_w4 = construct_work(6, "p1 w4", 0.1, [], person_id1, None)
        p1.work = [p1_w1, p1_w2, p1_w3, p1_w4]
        p1.topo_sort_work()
        self.assertTrue(p1.work.index(p1_w1) < p1.work.index(p1_w3))
        self.assertTrue(p1.work.index(p1_w4) < p1.work.index(p1_w1))
        return

