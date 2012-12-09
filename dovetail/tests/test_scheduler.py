import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.scheduler import Scheduler
from dovetail.projects.project import Project
from dovetail.work.work import Work
from dovetail.tests.util import construct_work

nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y")
nov2 = datetime.strptime("Nov 2, 2012", "%b %d, %Y")
nov5 = datetime.strptime("Nov 5, 2012", "%b %d, %Y")
nov6 = datetime.strptime("Nov 6, 2012", "%b %d, %Y")
nov15 = datetime.strptime("Nov 15, 2012", "%b %d, %Y")

class TestScheduler(unittest.TestCase):

    def test_construct_assignee_timelines(self):
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
        p1 = Project(1)
        p1_w1 = construct_work(1, "p1 w1", 1.0, [], person_id1, None)
        p1_w2 = construct_work(2, "p1 w2", 1.0, [], person_id1, None)
        p1_w3 = construct_work(5, "p1 w3", 0.1, [], person_id1, nov15)
        p1.work = [p1_w1, p1_w2, p1_w3]

        p2 = Project(2)
        p2_w1 = construct_work(3, "p2 w1", 1.0, [], person_id2, None)
        p2_w2 = construct_work(4, "p2 w2", 1.0, [2], person_id3, None)
        p2.work = [p2_w1, p2_w2]

        # Scheduler
        scheduler = Scheduler(nov1)
        projects = scheduler.schedule_projects([p1, p2])

        # Check work end dates
        self.assertEqual(nov2, p1_w1.est_end_date())
        self.assertEqual(nov5, p1_w2.est_end_date())
        self.assertEqual(nov2, p2_w1.est_end_date())
        self.assertEqual(nov6, p2_w2.est_end_date())

        # Check project end dates
        self.assertEqual(nov15, p1.est_end_date)
        self.assertEqual(nov6, p2.est_end_date)
        return

    def test_schedule_with_key_date_in_past(self):
        # Assignees
        person_id1 = 101

        # Projects
        p1 = Project(1)
        p1_w3 = construct_work(5, "p1 w3", 0.1, [], person_id1, nov1)
        p1.work = [p1_w3]

        # Scheduler
        scheduler = Scheduler(nov15)
        projects = scheduler.schedule_projects([p1])

        self.assertEqual(nov15, p1.est_end_date)
        return


