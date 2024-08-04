import unittest

import pandas as pd

from ts_scaler.data.utils import ensure_snake_case_columns


class TestEnsureSnakeCaseColumns(unittest.TestCase):
    def setUp(self):
        # Sample data with original column names
        data = {
            "Time Stamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "Time Zone": ["EST", "EST", "EST", "EST", "EST"],
            "Integrated Load": [100, 200, 150, 300, 400],
        }
        self.df = pd.DataFrame(data)
        self.column_mappings = {
            "Time Stamp": "time_stamp",
            "Time Zone": "time_zone",
            "Integrated Load": "integrated_load",
        }

    def test_ensure_snake_case_columns(self):
        # Apply the function to ensure snake_case columns
        result_df = ensure_snake_case_columns(self.df.copy(), self.column_mappings)

        # Expected column names after renaming
        expected_columns = ["time_stamp", "time_zone", "integrated_load"]

        # Compare the result columns with expected columns
        self.assertListEqual(list(result_df.columns), expected_columns)

    def test_missing_columns(self):
        # Test the function with a missing column mapping
        incomplete_mappings = {
            "Time Stamp": "time_stamp",
            # 'Time Zone': 'time_zone' is missing
            "Integrated Load": "integrated_load",
        }
        result_df = ensure_snake_case_columns(self.df.copy(), incomplete_mappings)

        # Expected column names after partial renaming
        expected_columns = ["time_stamp", "Time Zone", "integrated_load"]

        # Compare the result columns with expected columns
        self.assertListEqual(list(result_df.columns), expected_columns)


if __name__ == "__main__":
    unittest.main()
