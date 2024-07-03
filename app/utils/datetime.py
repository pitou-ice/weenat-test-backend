import pandas as pd


def dt_iso_format(df: pd.DataFrame, column: str):
    return df[column].apply(lambda t: pd.Timestamp(t).isoformat())
