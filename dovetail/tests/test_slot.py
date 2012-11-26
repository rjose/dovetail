import unittest
from mock import MagicMock
from dovetail.timeline.slot import Slot

class TestSlot(unittest.TestCase):

    def test_contains(self):
        slot = Slot(2, 7) # [2, 7]
        self.assertEqual(slot.contains(1, 2), False)
        self.assertEqual(slot.contains(1, 3), False)
        
        self.assertEqual(slot.contains(2, 3), True)
        self.assertEqual(slot.contains(2, 7), True)

        self.assertEqual(slot.contains(2, 7.5), False)
        self.assertEqual(slot.contains(7, 8), False)
        
    def test_fill(self):
        slot = Slot(2, 7) # [2, 7]
        # Should raise exception if trying to fill slot with something that doesn't fit
        self.assertRaises(Exception, slot.fill, 1, 2)

        # If fully fills slot, return empty array
        self.assertEqual(slot.fill(2, 7), [])

        self.assertEqual(slot.fill(2, 3), [Slot(3, 7)])
        self.assertEqual(slot.fill(3, 4), [Slot(2, 3), Slot(4, 7)])
        self.assertEqual(slot.fill(5, 7), [Slot(2, 5)])

# TODO: Check filling with an infinite end date

if __name__ == '__main__':
    unittest.main()
