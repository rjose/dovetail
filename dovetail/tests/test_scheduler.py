import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.scheduler import Scheduler
from dovetail.projects.project import Project
from dovetail.work.work import Work

class TestScheduler(unittest.TestCase):

    def test_construct_assignee_timelines(self):
        nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y") # Thu
        scheduler = Scheduler(nov1)
        t101 = scheduler.get_assignee_timeline(101)
        self.assertEqual(0, len(t101.dates))
        self.assertEqual(nov1, t101.cur_date)
        return
    
    def test_schedule_project(self):
        # Assignees
        person_id1 = 101
        person_id2 = 102
        person_id3 = 103

        # Projects
        p1 = Project()
        p1_w1 = Work(1, "p1 w1", 1.0, [], person_id1, None)
        p1_w2 = Work(2, "p1 w2", 1.0, [], person_id1, None)
        p1.work = [p1_w1, p1_w2]

        p2 = Project()
        p2_w1 = Work(3, "p2 w1", 1.0, [], person_id2, None)
        p2_w2 = Work(4, "p2 w2", 1.0, [2], person_id3, None)
        p2.work = [p2_w1, p2_w2]

        # Scheduler
        nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y")
        nov2 = datetime.strptime("Nov 2, 2012", "%b %d, %Y")
        nov5 = datetime.strptime("Nov 5, 2012", "%b %d, %Y")
        nov6 = datetime.strptime("Nov 6, 2012", "%b %d, %Y")
        scheduler = Scheduler(nov1)
        projects = scheduler.schedule_projects([p1, p2])

        # Check work end dates
        self.assertEqual(nov2, p1_w1.est_end_date())
        self.assertEqual(nov5, p1_w2.est_end_date())
        self.assertEqual(nov2, p2_w1.est_end_date())
        self.assertEqual(nov6, p2_w2.est_end_date())

        # Check project end dates
        self.assertEqual(nov5, p1.est_end_date)
        self.assertEqual(nov6, p2.est_end_date)
        return


