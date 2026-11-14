import unittest
from app.tables import internal_tables
from app.archive import verify_archive
from app.constraints import evaluate, violations
from app.store import load_case


class TableTests(unittest.TestCase):
    def test_overlapping_totals_are_consistent(self):
        case = load_case('standard')
        tables = internal_tables(case)
        county = {cell['id']: cell['value'] for cell in tables['county']}
        self.assertEqual(county['total-boxes'], county['north-boxes'] + county['south-boxes'])

    def test_negative_volume_breaks_business_domain(self):
        case = load_case('standard')
        values = {**case['variables'], 'a_boxes': -1}
        self.assertIn('bound:a_boxes', violations(case, values))

    def test_archive_cannot_be_overwritten(self):
        case = load_case('standard')
        case['variables']['old_a_boxes'] = 16
        self.assertEqual(verify_archive(case), ['old-north'])
