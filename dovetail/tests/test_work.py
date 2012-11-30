import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.timeline.timeline import Timeline
from dovetail.timeline.slot import Slot
from dovetail.work.work import Work

class TestWork(unittest.TestCase):

    def test_schedule(self):
        nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y") # Thu
        nov7 = datetime.strptime("Nov 7, 2012", "%b %d, %Y") # Wed
        nov8 = datetime.strptime("Nov 8, 2012", "%b %d, %Y") # Thu
        timeline = Timeline(nov1)
        work_slot, _ = timeline.find_slot(4, 1.5)

        w = Work(1, 'Some work', 1.5, [], 100, None)
        w.schedule(work_slot)
        self.assertEqual(nov7, w.est_start_date())
        self.assertEqual(nov8, w.est_end_date())
        return

    def test_earliest_start_date(self):
        nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y") # Thu
        nov5 = datetime.strptime("Nov 5, 2012", "%b %d, %Y") # Mon
        nov7 = datetime.strptime("Nov 7, 2012", "%b %d, %Y") # Wed
        timeline = Timeline(nov1)
        work_slot, _ = timeline.find_slot(4, 1.5)

        w1 = Work(1, 'w1', 1.0, [], 100, None)
        w1.schedule(timeline.find_slot(0, 1)[0])

        w2 = Work(2, 'w2', 1.0, [], 101, None)
        w2.schedule(timeline.find_slot(1, 3)[0])

        w3 = Work(3, 'w3', 1.0, [1, 2], 200, None)

        work_dict = {1: w1, 2: w2, 3: w3}
        self.assertEqual(nov7, w3.earliest_start_date(work_dict, nov1))
        return
