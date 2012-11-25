import unittest
from mock import MagicMock
import dovetail.projects.models as projects
import dovetail.people.models as people

class TestEditProjectWork(unittest.TestCase):

    def test_parse_workline(self):
        # Mock out person lookup
        people.get_person_from_name = MagicMock(return_value = {'id': 21})
        connection = None

        workline = '[1, "Borvo Borvison", "0.20 d", "Make title longer", [], "?"]'
        work_data = projects.parse_workline(connection, workline)
        fields = work_data['fields']
        self.assertEqual(work_data['id'], 1)
        self.assertEqual(fields['assignee'], 21)
        self.assertEqual(fields['effort_left_d'], 0.2)
        self.assertEqual(fields['title'], 'Make title longer')
        self.assertEqual(fields['prereqs'], [])
        self.assertEqual(fields['key_date'], None)


# TODO: Test prereqs and key date
# TODO: Test invalid input
if __name__ == '__main__':
    unittest.main()
