import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.charts.support.gantt import Gantt
import dovetail.tests.util as util

class TestGantt(unittest.TestCase):

    def test_compute_dates(self):
        gantt = Gantt(util.nov1, [], util.nov23)
        self.assertEqual([util.nov5, util.nov12, util.nov19], gantt.tick_dates)
        return

    def test_compute_date_labels(self):
        gantt = Gantt(util.nov1, [], util.nov23)
        self.assertEqual([
            {'label': 'Nov 05, 2012', 'x': 180},
            {'label': 'Nov 12, 2012', 'x': 320},
            {'label': 'Nov 19, 2012', 'x': 460}], gantt.date_labels())
        return
