import unittest
from dovetail.tests.test_edit_project_work import TestEditProjectWork
from dovetail.tests.test_slot import TestSlot
from dovetail.tests.test_timeline import TestTimeline
from dovetail.tests.test_work import TestWork
from dovetail.tests.test_scheduler import TestScheduler
from dovetail.tests.test_project import TestProject
from dovetail.tests.test_gantt import TestGantt

alltests = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(t) for t in [
        TestEditProjectWork,
        TestSlot,
        TestTimeline,
        TestWork,
        TestScheduler,
        TestProject,
        TestGantt
        ]])

unittest.TextTestRunner(verbosity=2).run(alltests)
