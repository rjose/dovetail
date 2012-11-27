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

