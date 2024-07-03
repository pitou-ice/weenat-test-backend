import pandas as pd
from datetime import datetime

from core.database import engine
from core.enums import Columns, Tables
from utils.datetime import dt_iso_format


def append_data_records(data_records: pd.DataFrame) -> None:
    data_records.to_sql(
        Tables.DATA_RECORD.value,
        engine,
        if_exists='append',
        index=False
    )


def get_all_records_by_datalogger_in_datetime(
    datalogger: str,
    since: str | None = None,
    before: str | None = None
) -> pd.DataFrame:
    data_records = pd.read_sql(
        f'''
        SELECT *
        FROM {Tables.DATA_RECORD.value}
        WHERE {Columns.DATALOGGER.value}="{datalogger}"
        AND {Columns.MEASURED_AT.value}
        BETWEEN "{pd.to_datetime(since or 0)}"
        AND "{pd.to_datetime(before or datetime.now())}"
        ''',
        engine
    )
    data_records[Columns.MEASURED_AT.value] = \
        dt_iso_format(data_records, Columns.MEASURED_AT.value)
    return data_records
