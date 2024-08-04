from typing import Optional

import pandas as pd


class MovingAverageCalculator:
    def __init__(self, window_size: int = 7):
        self.window_size = window_size

    def calculate(
        self,
        df: pd.DataFrame,
        time_column: str,
        value_column: str,
        ma_column: Optional[str] = "moving_average",
        std_column: Optional[str] = "moving_standard_deviation",
    ) -> pd.DataFrame:
        if time_column not in df.columns or value_column not in df.columns:
            raise ValueError(
                f"DataFrame must contain '{time_column}' and '{value_column}' columns."
            )

        df[time_column] = pd.to_datetime(df[time_column])
        df.set_index(time_column, inplace=True)

        df[ma_column] = df[value_column].rolling(window=self.window_size).mean()
        df[std_column] = df[value_column].rolling(window=self.window_size).std()

        return df.reset_index()
