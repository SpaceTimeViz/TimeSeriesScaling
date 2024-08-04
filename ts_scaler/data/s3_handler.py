import logging
import os
from typing import Optional

import boto3

from ts_scaler.utils.logger import setup_logger


class S3Handler:
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or setup_logger(__name__)
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.check_credentials()

    def check_credentials(self):
        try:
            self.s3.meta.client.head_bucket(Bucket=self.bucket_name)
            self.logger.info(f"Access to bucket '{self.bucket_name}' verified.")
        except Exception as e:
            self.logger.error(f"Failed to access bucket: {e}")

    def download_files(self, s3_path: str, local_dir: str):
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            self.logger.info(f"Created local folder {local_dir}.")

        # If a specific file is specified, download it directly
        if s3_path.endswith(".csv"):
            target = os.path.join(local_dir, os.path.basename(s3_path))
            self.logger.debug(f"Downloading {s3_path} to {target}")
            try:
                self.bucket.download_file(s3_path, target)
                self.logger.info(f"Downloaded {s3_path} to {target}")
            except Exception as e:
                self.logger.error(f"Failed to download {s3_path} to {target}: {e}")
        else:
            # Otherwise, download all files in the specified folder
            for obj in self.bucket.objects.filter(Prefix=s3_path):
                relative_path = os.path.relpath(obj.key, s3_path)
                target = os.path.join(local_dir, relative_path)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                self.logger.debug(f"Downloading {obj.key} to {target}")
                try:
                    self.bucket.download_file(obj.key, target)
                    self.logger.info(f"Downloaded {obj.key} to {target}")
                except Exception as e:
                    self.logger.error(f"Failed to download {obj.key} to {target}: {e}")

    def upload_file(self, file_path: str, s3_path: str):
        try:
            self.bucket.upload_file(file_path, s3_path)
            self.logger.info(
                f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_path}"
            )
        except Exception as e:
            self.logger.error(
                f"Failed to upload {file_path} to s3://{self.bucket_name}/{s3_path}: {e}"
            )

    def check_bucket_status(self):
        self.logger.info(
            f"Bucket '{self.bucket_name}' exists and contains the following objects:"
        )
        for obj in self.bucket.objects.all():
            self.logger.info(f"- {obj.key}")

    def upload_folder(self, folder_path: str, s3_folder: str):
        for root, _, files in os.walk(folder_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, folder_path)
                s3_path = os.path.join(s3_folder, relative_path)
                try:
                    self.bucket.upload_file(local_path, s3_path)
                    self.logger.info(
                        f"Uploaded {local_path} to s3://{self.bucket_name}/{s3_path}"
                    )
                except Exception as e:
                    self.logger.error(
                        f"Failed to upload {local_path} to s3://{self.bucket_name}/{s3_path}: {e}"
                    )

    def rename_folder(self, old_prefix: str, new_prefix: str):
        for obj in self.bucket.objects.filter(Prefix=old_prefix):
            copy_source = {"Bucket": self.bucket_name, "Key": obj.key}
            new_key = obj.key.replace(old_prefix, new_prefix, 1)
            try:
                self.bucket.copy(copy_source, new_key)
                self.logger.info(
                    f"Renamed {obj.key} to {new_key} in s3://{self.bucket_name}"
                )
            except Exception as e:
                self.logger.error(f"Failed to rename {obj.key} to {new_key}: {e}")
        try:
            self.bucket.delete_objects(
                Delete={
                    "Objects": [
                        {"Key": obj.key}
                        for obj in self.bucket.objects.filter(Prefix=old_prefix)
                    ]
                }
            )
        except Exception as e:
            self.logger.error(f"Failed to delete objects with prefix {old_prefix}: {e}")
