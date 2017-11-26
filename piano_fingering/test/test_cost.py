from unittest import TestCase
from ..cost import createCostDatabase


class TestCostDatabases(TestCase):

    def test_creation(self):
        right_hand_cost_database, left_hand_cost_database = createCostDatabase()
        self.assertEqual(5 * 88 * 5 * 88, len(right_hand_cost_database))
        self.assertEqual(5 * 88 * 5 * 88, len(left_hand_cost_database))
