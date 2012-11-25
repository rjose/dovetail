import unittest
from dovetail.tests.test_edit_project_work import TestEditProjectWork

suite = unittest.TestLoader().loadTestsFromTestCase(TestEditProjectWork)
unittest.TextTestRunner(verbosity=2).run(suite)
