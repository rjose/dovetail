import unittest
from mock import MagicMock
from datetime import datetime
from dovetail.timeline.timeline import Timeline
from dovetail.timeline.slot import Slot
from dovetail.work.work import Work
import dovetail.work.db as work_db
import dovetail.tests.util as util

class TestWork(unittest.TestCase):

    def test_schedule(self):
        timeline = Timeline(util.nov1)
        work_slot, _ = timeline.find_slot(4, 1.5)

        w = Work(1)
        w.title = 'Some work'
        w.effort_left_d = 1.5
        w.assignee_id = 100

        w.schedule(work_slot)
        self.assertEqual(util.nov7, w.est_start_date())
        self.assertEqual(util.nov8, w.est_end_date())
        return

    def test_earliest_start_date(self):
        timeline = Timeline(util.nov1)
        work_slot, _ = timeline.find_slot(4, 1.5)

        w1 = Work(1)
        w1.title = 'w1'
        w1.effort_left_d = 1.0
        w1.assignee_id = 100
        w1.schedule(timeline.find_slot(0, 1)[0])

        w2 = Work(2)
        w2.title = 'w2'
        w2.effort_left_d = 1.0
        w2.assignee_id = 101
        w2.schedule(timeline.find_slot(1, 3)[0])

        w3 = Work(3)
        w3.title = 'w3'
        w3.effort_left_d = 1.0
        w3.prereqs = [1, 2]
        w3.assignee_id = 200

        work_dict = {1: w1, 2: w2, 3: w3}
        self.assertEqual(util.nov7, w3.earliest_start_date(work_dict, util.nov1))
        return

    def test_fields_to_work_object(self):
        w1 = work_db.fields_to_work_object({
            'id': 25,
            'title': 'w1',
            'effort_left_d': 16.7,
            'prereqs': '[1, 2]',
            'assignee_id': 100,
            'key_date': '2012-12-12'
        })
        self.assertEqual([25, 'w1', 16.7, [1, 2], 100, datetime(2012, 12, 12)],
                [w1.work_id, w1.title, w1.effort_left_d, w1.prereqs, w1.assignee_id, w1.key_date])
        return

