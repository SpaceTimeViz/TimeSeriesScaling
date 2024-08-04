import logging
import os
import unittest
from unittest.mock import MagicMock, patch

from ts_scaler.data.s3_handler import S3Handler

class TestS3Handler(unittest.TestCase):

    @patch("boto3.resource")
    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_download_files_with_existing_local_dir(
        self, mock_makedirs, mock_exists, mock_boto_resource
    ):
        # Setup
        mock_exists.return_value = True
        mock_bucket = MagicMock()
        mock_boto_resource.return_value.Bucket.return_value = mock_bucket

        # Mock objects to return when filter is called
        mock_bucket.objects.filter.return_value = [
            MagicMock(key="test_prefix/image1.jpg"),
            MagicMock(key="test_prefix/image2.png"),
        ]

        # Instantiate the S3Handler
        s3_handler = S3Handler()
        s3_handler.download_files("test_prefix/", "test_local_dir/")

        # Assertions
        mock_bucket.download_file.assert_any_call(
            "test_prefix/image1.jpg", "test_local_dir/image1.jpg"
        )
        mock_bucket.download_file.assert_any_call(
            "test_prefix/image2.png", "test_local_dir/image2.png"
        )

    @patch("boto3.resource")
    @patch.dict(os.environ, {"S3_BUCKET_NAME": "test_bucket"})
    def test_rename_folder(self, mock_boto_resource):
        # Setup
        mock_bucket = MagicMock()
        mock_boto_resource.return_value.Bucket.return_value = mock_bucket
        mock_bucket.objects.filter.return_value = [
            MagicMock(key="test_prefix/image1.jpg"),
            MagicMock(key="test_prefix/image2.png"),
        ]

        # Instantiate the S3Handler
        s3_handler = S3Handler()

        # Call rename_folder
        s3_handler.rename_folder("test_prefix/", "new_test_prefix/")

        # Assertions
        mock_bucket.copy.assert_any_call(
            {"Bucket": "test_bucket", "Key": "test_prefix/image1.jpg"},
            "new_test_prefix/image1.jpg",
        )
        mock_bucket.copy.assert_any_call(
            {"Bucket": "test_bucket", "Key": "test_prefix/image2.png"},
            "new_test_prefix/image2.png",
        )
        self.assertEqual(mock_bucket.objects.filter.call_count, 2)
        mock_bucket.delete_objects.assert_called_once_with(
            Delete={
                "Objects": [
                    {"Key": "test_prefix/image1.jpg"},
                    {"Key": "test_prefix/image2.png"}
                ]
            }
        )

if __name__ == "__main__":
    unittest.main()