import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.scheduler import Scheduler
from dovetail.projects.project import Project

# TODO: Write a helper function to construct work for a project

class TestScheduler(unittest.TestCase):

    def test_construct_assignee_timelines(self):
        nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y") # Thu
        scheduler = Scheduler(nov1)
        t101 = scheduler.get_assignee_timeline(101)
        self.assertEqual(0, len(t101.dates))
        self.assertEqual(nov1, t101.cur_date)
        return
    

