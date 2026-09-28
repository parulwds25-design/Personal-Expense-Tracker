import unittest
import os
from main1 import ExpenseTracker


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_expenses.csv"

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        self.tracker = ExpenseTracker(self.test_file)

    def test_file_created(self):
        self.assertTrue(os.path.exists(self.test_file))

    def test_total_expense(self):
        with open(self.test_file, "a") as file:
            file.write("2026-09-15,Food,100,Lunch\n")
            file.write("2026-09-16,Travel,200,Bus\n")

        total = self.tracker.total_expense()

        self.assertEqual(total, 300)


if __name__ == "__main__":
    unittest.main()
