import unittest

import pandas as pd

from ts_scaler.scaler.moving_average import MovingAverageCalculator


class TestMovingAverageCalculator(unittest.TestCase):
    def setUp(self):
        # Sample data
        data = {
            "time_stamp": pd.date_range(start="2023-01-01", periods=10, freq="D"),
            "integrated_load": [100, 200, 150, 300, 400, 500, 250, 100, 150, 200],
        }
        self.df = pd.DataFrame(data)
        self.calculator = MovingAverageCalculator(window_size=3)

    def test_calculate_moving_average_and_std(self):
        # Calculate moving average and standard deviation
        result_df = self.calculator.calculate(
            self.df, time_column="time_stamp", value_column="integrated_load"
        )

        # Expected results (shifted by one to match the shift in the method)
        expected_moving_average = [
            None,
            None,
            None,
            150.0,
            216.67,
            283.33,
            400.0,
            383.33,
            283.33,
            166.67,
        ]
        expected_moving_std = [
            None,
            None,
            None,
            50.0,
            76.38,
            125.83,
            100.0,
            125.83,
            202.07,
            76.38,
        ]

        # Convert expected results to Series with the same index as the result
        expected_moving_average_series = pd.Series(
            expected_moving_average, index=result_df.index
        ).round(2)
        expected_moving_std_series = pd.Series(
            expected_moving_std, index=result_df.index
        ).round(2)

        # Compare results
        pd.testing.assert_series_equal(
            result_df["moving_average"].round(2),
            expected_moving_average_series,
            check_names=False,
        )
        pd.testing.assert_series_equal(
            result_df["moving_standard_deviation"].round(2),
            expected_moving_std_series,
            check_names=False,
        )

    def test_missing_columns(self):
        # Test missing time column
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate(
                self.df, time_column="missing_time", value_column="integrated_load"
            )
        self.assertTrue(
            "DataFrame must contain 'missing_time' and 'integrated_load' columns."
            in str(context.exception)
        )

        # Test missing value column
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate(
                self.df, time_column="time_stamp", value_column="missing_value"
            )
        self.assertTrue(
            "DataFrame must contain 'time_stamp' and 'missing_value' columns."
            in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
