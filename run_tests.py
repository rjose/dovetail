import unittest
from dovetail.tests.test_edit_project_work import TestEditProjectWork
from dovetail.tests.test_slot import TestSlot
from dovetail.tests.test_timeline import TestTimeline
from dovetail.tests.test_work import TestWork

suite_edit_project_work = unittest.TestLoader().loadTestsFromTestCase(TestEditProjectWork)
suite_slot = unittest.TestLoader().loadTestsFromTestCase(TestSlot)
suite_timeline = unittest.TestLoader().loadTestsFromTestCase(TestTimeline)
suite_work = unittest.TestLoader().loadTestsFromTestCase(TestWork)

unittest.TextTestRunner(verbosity=2).run(suite_timeline)
