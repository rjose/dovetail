import unittest
import dovetail.projects.models as projects

class TestEditProjectWork(unittest.TestCase):

    def test_parse_workline(self):
        workline = '[1, "Borvo Borvison", "0.20 d", "Make title longer", [], "?"]'
        work_data = projects.parse_workline(workline)
        fields = work_data['fields']
        self.assertEqual(work_data['id'], 1)
        self.assertEqual(fields['assignee'], "Borvo Borvison")
        self.assertEqual(fields['effort_left_d'], 0.2)
        self.assertEqual(fields['title'], 'Make title longer')
        self.assertEqual(fields['prereqs'], [])
        self.assertEqual(fields['key_date'], None)


# TODO: Test prereqs and key date
# TODO: Test invalid input
if __name__ == '__main__':
    unittest.main()
