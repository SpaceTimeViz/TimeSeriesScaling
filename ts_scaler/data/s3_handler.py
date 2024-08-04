import logging
import os
from typing import Optional

import boto3

from ts_scaler.utils.logger import setup_logger

class S3Handler:
    def __init__(self, s3_image_folder: str, local_dir: str, logger: Optional[logging.Logger] = None) -> None:
        self.s3_image_folder = s3_image_folder
        self.local_dir = local_dir
        self.logger = logger or setup_logger(__name__)
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.bucket = boto3.resource("s3").Bucket(self.bucket_name)

    def download_images(self):
        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)
            self.logger.info(f"Created local folder {self.local_dir}.")
        for obj in self.bucket.objects.filter(Prefix=self.s3_image_folder):
            target = os.path.join(self.local_dir, os.path.basename(obj.key))
            self.bucket.download_file(obj.key, target)
            self.logger.info(f"Downloaded {obj.key} to {target}")

    def upload_file(self, file_path: str, s3_path: str):
        self.bucket.upload_file(file_path, s3_path)
        self.logger.info(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_path}")

    def check_bucket_status(self):
        self.logger.info(f"Bucket '{self.bucket_name}' exists and contains the following objects:")
        for obj in self.bucket.objects.all():
            self.logger.info(f"- {obj.key}")

    def upload_folder(self, folder_path: str, s3_folder: str):
        for root, _, files in os.walk(folder_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, folder_path)
                s3_path = os.path.join(s3_folder, relative_path)
                self.bucket.upload_file(local_path, s3_path)
                self.logger.info(f"Uploaded {local_path} to s3://{self.bucket_name}/{s3_path}")

    def rename_folder(self, old_prefix: str, new_prefix: str):
        for obj in self.bucket.objects.filter(Prefix=old_prefix):
            copy_source = {"Bucket": self.bucket_name, "Key": obj.key}
            new_key = obj.key.replace(old_prefix, new_prefix, 1)
            self.bucket.copy(copy_source, new_key)
            self.logger.info(f"Renamed {obj.key} to {new_key} in s3://{self.bucket_name}")
        self.bucket.delete_objects(
            Delete={
                "Objects": [
                    {"Key": obj.key}
                    for obj in self.bucket.objects.filter(Prefix=old_prefix)
                ]
            }
        )
