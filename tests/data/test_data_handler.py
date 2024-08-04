import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

from ts_scaler.data.data_handler import DataHandler


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame
        data = {
            "Time Stamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "Time Zone": ["EST", "EST", "EST", "EST", "EST"],
            "Integrated Load": [100, 200, 150, 300, 400],
        }
        self.df = pd.DataFrame(data)

    @patch("ts_scaler.data.data_handler.os.path.exists")
    @patch("ts_scaler.data.data_handler.pd.read_csv")
    @patch("ts_scaler.data.data_handler.S3Handler")
    def test_fetch_nyiso_data_files_exist(
        self, mock_s3_handler, mock_read_csv, mock_exists
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup the mocks
            mock_s3_handler.return_value
            mock_exists.return_value = True
            mock_read_csv.return_value = self.df

            data_handler = DataHandler()

            # Call the method to test
            result_df = data_handler.fetch_nyiso_data(tmpdir, "20230101", "20230105")

            # Assertions
            self.assertEqual(len(mock_read_csv.call_args_list), 5)
            self.assertEqual(len(result_df), 25)  # 5 days * 5 rows per day
            self.assertListEqual(
                list(result_df.columns), ["time_stamp", "time_zone", "integrated_load"]
            )

    @patch("ts_scaler.data.data_handler.os.path.exists")
    @patch("ts_scaler.data.data_handler.pd.read_csv")
    @patch("ts_scaler.data.data_handler.S3Handler")
    def test_fetch_nyiso_data_no_files(
        self, mock_s3_handler, mock_read_csv, mock_exists
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup the mocks
            mock_s3_handler.return_value
            mock_exists.return_value = False
            mock_read_csv.side_effect = FileNotFoundError

            data_handler = DataHandler()

            # Assertions
            with self.assertRaises(ValueError) as context:
                data_handler.fetch_nyiso_data(tmpdir, "20230101", "20230105")
            self.assertTrue(
                "No data files found for the date range" in str(context.exception)
            )


if __name__ == "__main__":
    unittest.main()
