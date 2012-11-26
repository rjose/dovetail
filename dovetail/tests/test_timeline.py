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

        # TODO: Test where prefered slot is not available

    def test_claim_slot(self):
        timeline = Timeline(datetime.now())
        timeline.claim_slot(Slot(4, 4.5), 0)
        self.assertEqual([Slot(0, 4), Slot(4.5, float('inf'))], timeline.slots)
        
if __name__ == '__main__':
    unittest.main()

