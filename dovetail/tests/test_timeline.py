import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.timeline.timeline import Timeline
from dovetail.timeline.slot import Slot

class TestTimeline(unittest.TestCase):

    def test_find_slot(self):
        timeline = Timeline(datetime.now())
        my_slot, containing_slot_index = timeline.find_slot(4, 0.5)
        self.assertEqual(Slot(4, 4.5), my_slot)
        self.assertEqual(0, containing_slot_index)

        # Test where prefered slot is not available
        timeline.slots = [Slot(1, 3), Slot(4, float('inf'))]
        my_slot, containing_slot_index = timeline.find_slot(0, 2.5)
        self.assertEqual(Slot(4, 6.5), my_slot)
        self.assertEqual(1, containing_slot_index)

    def test_claim_slot(self):
        timeline = Timeline(datetime.now())
        timeline.claim_slot(Slot(4, 4.5), 0)
        self.assertEqual([Slot(0, 4), Slot(4.5, float('inf'))], timeline.slots)
        return

    def test_add_dates(self):
        nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y") # Thu
        nov2 = datetime.strptime("Nov 2, 2012", "%b %d, %Y") # Fri
        nov3 = datetime.strptime("Nov 3, 2012", "%b %d, %Y") # Sat
        nov5 = datetime.strptime("Nov 5, 2012", "%b %d, %Y") # Mon

        timeline = Timeline(nov1)
        timeline.add_dates(nov1)
        self.assertEqual([nov1], timeline.dates)

        timeline.add_dates(nov2)
        self.assertEqual([nov1, nov2], timeline.dates)

        # Check idempotent
        timeline.add_dates(nov2)
        self.assertEqual([nov1, nov2], timeline.dates)

        # Skip until next workday
        timeline.add_dates(nov3)
        self.assertEqual([nov1, nov2, nov5], timeline.dates)
        return

    def test_day_from_date(self):
        nov1 = datetime.strptime("Nov 1, 2012", "%b %d, %Y") # Thu
        nov2 = datetime.strptime("Nov 2, 2012", "%b %d, %Y") # Fri
        nov3 = datetime.strptime("Nov 3, 2012", "%b %d, %Y") # Sat
        nov4 = datetime.strptime("Nov 4, 2012", "%b %d, %Y") # Sun
        nov5 = datetime.strptime("Nov 5, 2012", "%b %d, %Y") # Mon

        timeline = Timeline(nov1)
        self.assertEqual(0, timeline.day_from_date(nov1))
        self.assertEqual(1, timeline.day_from_date(nov2))
        self.assertEqual(2, timeline.day_from_date(nov3))
        self.assertEqual(2, timeline.day_from_date(nov4))
        self.assertEqual(2, timeline.day_from_date(nov5))
        return

        
if __name__ == '__main__':
    unittest.main()

