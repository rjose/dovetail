import unittest
from dovetail.tests.test_edit_project_work import TestEditProjectWork
from dovetail.tests.test_slot import TestSlot
from dovetail.tests.test_timeline import TestTimeline

suite_edit_project_work = unittest.TestLoader().loadTestsFromTestCase(TestEditProjectWork)
suite_slot = unittest.TestLoader().loadTestsFromTestCase(TestSlot)
suite_timeline = unittest.TestLoader().loadTestsFromTestCase(TestTimeline)

unittest.TextTestRunner(verbosity=2).run(suite_timeline)
