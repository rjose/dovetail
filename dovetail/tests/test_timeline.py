import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.timeline.timeline import Timeline
from dovetail.timeline.slot import Slot
from datetime import timedelta
import dovetail.tests.util as util

class TestTimeline(unittest.TestCase):

    def test_add_dates_to(self):
        timeline = Timeline(util.nov1)
        timeline.add_dates_to(util.nov1)
        self.assertEqual([util.nov1], timeline.dates)

        timeline.add_dates_to(util.nov2)
        self.assertEqual([util.nov1, util.nov2], timeline.dates)

        # Check idempotent
        timeline.add_dates_to(util.nov2)
        self.assertEqual([util.nov1, util.nov2], timeline.dates)

        # Skip until next workday
        timeline.add_dates_to(util.nov3)
        self.assertEqual([util.nov1, util.nov2, util.nov5], timeline.dates)
        return

    def test_day_from_date(self):
        timeline = Timeline(util.nov1)
        self.assertEqual(0, timeline.day_from_date(util.nov1))
        self.assertEqual(1, timeline.day_from_date(util.nov2))
        self.assertEqual(2, timeline.day_from_date(util.nov3))
        self.assertEqual(2, timeline.day_from_date(util.nov4))
        self.assertEqual(2, timeline.day_from_date(util.nov5))
        return

    def test_add_days(self):
       timeline = Timeline(util.nov1)
       timeline.add_days_to(0)
       self.assertEqual([util.nov1], timeline.dates)

       timeline.add_days_to(2)
       self.assertEqual([util.nov1, util.nov2, util.nov5], timeline.dates)
       return

    def test_date_from_day(self):
       timeline = Timeline(util.nov1)
       self.assertEqual(util.nov5, timeline.date_from_day(2))
       self.assertEqual(util.nov5, timeline.date_from_day(2.9))
       return

    def test_find_slot(self):
        timeline = Timeline(util.nov1)
        my_slot, containing_slot_index = timeline.find_slot(4, 0.5)
        self.assertEqual(Slot(4, 4.5), my_slot)
        self.assertEqual(0, containing_slot_index)

        # Test where prefered slot is not available
        timeline.slots = [Slot(1, 3), Slot(4, float('inf'))]
        my_slot, containing_slot_index = timeline.find_slot(0, 2.5)
        self.assertEqual(Slot(4, 6.5), my_slot)
        self.assertEqual(1, containing_slot_index)

        # Check that the slot dates are correct
        self.assertEqual(util.nov7, my_slot.start_date)
        self.assertEqual(util.nov9, my_slot.end_date)
        return

    # This tests the case where the final, infinite slot needs to be used
    # but the desired slot does not fit without modification (smoke test)
    def test_find_slot_at_end(self):
        timeline = Timeline(util.nov1)
        timeline.claim_slot(Slot(0, 1.0), 0)
        my_slot, containing_slot_index = timeline.find_slot(0, 1.0)
        return


    def test_claim_slot(self):
        timeline = Timeline(util.nov1)
        timeline.claim_slot(Slot(4, 4.5), 0)
        self.assertEqual([Slot(0, 4), Slot(4.5, float('inf'))], timeline.slots)
        return

    def test_claim_slot_on_partially_filled_days(self):
        timeline = Timeline(util.nov1)
        timeline.claim_slot(Slot(4, 4.5), 0)
        my_slot, containing_slot_index = timeline.find_slot(4.1, 0.5)
        self.assertEqual(Slot(4.5, 5), my_slot)
        return


    def test_find_slot_with_ending_date(self):
        timeline = Timeline(util.nov1)
        my_slot, containing_slot_index = timeline.find_slot_with_ending_date(util.nov7, 0.1)
        self.assertEqual(Slot(4.4, 4.5), my_slot)
        return

    def test_find_slot_with_ending_date2(self):
        # This tests an infinite loop case
        delta1 = timedelta(0.25)
        timeline = Timeline(util.nov1 + delta1)
        my_slot, containing_slot_index = timeline.find_slot_with_ending_date(util.nov7, 0.1)
        self.assertEqual(Slot(4.4, 4.5), my_slot)
        return

        
if __name__ == '__main__':
    unittest.main()

