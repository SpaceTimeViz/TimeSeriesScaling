import logging
import os
import unittest
from unittest.mock import MagicMock, patch

from ts_scaler.data.s3_handler import S3Handler
from ts_scaler.data.data_handler import DataHandler

class TestDataHandler(unittest.TestCase):

    @patch("ts_scaler.data.s3_handler.S3Handler")
    def test_download_nyiso_all_files(self, mock_s3_handler):
        # Mock the S3Handler instance
        mock_instance = mock_s3_handler.return_value

        # Instantiate the DataHandler
        data_handler = DataHandler()

        # Call the method to test
        data_handler.download_nyiso()

        # Assertions
        mock_instance.download_files.assert_called_once_with("NYISO/", "./data")

    @patch("ts_scaler.data.s3_handler.S3Handler")
    def test_download_nyiso_specific_date(self, mock_s3_handler):
        # Mock the S3Handler instance
        mock_instance = mock_s3_handler.return_value

        # Instantiate the DataHandler
        data_handler = DataHandler()

        # Call the method to test with a specific date
        data_handler.download_nyiso(date="20010601")

        # Assertions
        mock_instance.download_files.assert_called_once_with("NYISO/20010601palIntegrated_csv/", "./data")

if __name__ == "__main__":
    unittest.main()
