import pandas as pd


def ensure_snake_case_columns(df: pd.DataFrame, column_mappings: dict) -> pd.DataFrame:
    """Ensure the DataFrame has consistent snake_case column names."""
    df.rename(columns=column_mappings, inplace=True)
    return df
