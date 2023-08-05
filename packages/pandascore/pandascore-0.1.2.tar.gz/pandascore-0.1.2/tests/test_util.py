import unittest

from pandascore.util import format_params

class TestUtils(unittest.TestCase):

    def test_invalid_params(self):
        valid_params = ['videogame_id', 'league_id']

        expected_result = {'videogame_id': 1}
        actual_result = format_params(valid_params, videogame_id=1)

        self.assertEqual(expected_result, actual_result)

    def test_empty_params(self):
        valid_params = ['videogame_id', 'league_id']

        expected_result = {'league_id': 1}
        actual_result = format_params(valid_params, videogame_id=None, league_id=1)

        self.assertEqual(expected_result, actual_result)

    def test_filter_params(self):
        valid_params = ['filter']

        expected_result = {'filter[created_at]': 'test', 'filter[name]': 'test'}
        actual_result = format_params(valid_params, filter="name=test;created_at=test")

        self.assertEqual(expected_result, actual_result)

    def test_range_params(self):
        valid_params = ['range']

        expected_result = {'range[created_at]': '2017-01-01,2017-02-01'}
        actual_result = format_params(valid_params, range="created_at=2017-01-01,2017-02-01")

        self.assertEqual(expected_result, actual_result)
