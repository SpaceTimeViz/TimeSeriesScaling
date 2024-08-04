import os
import glob
import pandas as pd
import logging
from typing import Optional, List
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ts_scaler.data.s3_handler import S3Handler
from ts_scaler.utils.logger import setup_logger

# Setup logger and load environment variables
logger = setup_logger()
load_dotenv()


class DataHandler:
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or setup_logger(__name__)
        self.s3_handler = S3Handler(logger=self.logger)

    def fetch_nyiso_data(self, local_dir: str = "./data", start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Download NYISO data to the specified local directory for a date range."""
        if not start_date or not end_date:
            raise ValueError("Both start_date and end_date must be provided in YYYYMMDD format.")

        start_date_dt = datetime.strptime(start_date, '%Y%m%d')
        end_date_dt = datetime.strptime(end_date, '%Y%m%d')

        if start_date_dt > end_date_dt:
            raise ValueError("start_date must be earlier than or equal to end_date.")

        current_date_dt = start_date_dt
        all_data_frames = []

        while current_date_dt <= end_date_dt:
            current_date_str = current_date_dt.strftime('%Y%m%d')
            folder = f"NYISO/{current_date_str[:6]}01palIntegrated_csv/"
            target_file = f"{current_date_str}palIntegrated.csv"
            local_file_path = os.path.join(local_dir, target_file)

            if os.path.exists(local_file_path):
                self.logger.info(f"Data for date {current_date_str} already exists locally. Reading the data.")
                all_data_frames.append(pd.read_csv(local_file_path))
            else:
                self.logger.info(f"Data for date {current_date_str} not found locally. Downloading from S3.")
                self.s3_handler.download_files(os.path.join(folder, target_file), local_dir)
                if os.path.exists(local_file_path):
                    self.logger.info(f"Successfully downloaded data for date {current_date_str}. Reading the data.")
                    all_data_frames.append(pd.read_csv(local_file_path))
                else:
                    self.logger.error(f"Failed to download data for date {current_date_str} from S3.")

            current_date_dt += timedelta(days=1)

        if not all_data_frames:
            raise ValueError(
                f"No data files found for the date range {start_date} to {end_date}. Please check the dates or directory.")

        combined_df = pd.concat(all_data_frames, ignore_index=True)
        return combined_df


if __name__ == "__main__":
    data_handler = DataHandler()
    try:
        df = data_handler.fetch_nyiso_data("data", "20230101", "20230105")
        print(df.head())
    except ValueError as e:
        print(f"Error: {e}")