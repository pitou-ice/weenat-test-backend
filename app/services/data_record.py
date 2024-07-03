import pandas as pd

from core.enums import Columns
from schemas.data_record_request import DataRecordRequest


TIME_SPANS = {
    'minute': 'min',
    'hour': 'h',
    'day': 'D',
}


def extract_data(data_records: list[DataRecordRequest]) -> pd.DataFrame:
    data_record_df1 = pd.DataFrame(
        [log.model_dump() for log in data_records],
        columns=[
            Columns.DATALOGGER.value,
            Columns.AT.value,
            Columns.MEASUREMENTS.value
        ])
    data_record_df2 = pd.DataFrame(
        data_record_df1[Columns.MEASUREMENTS.value].to_list(),
        columns=[
            Columns.PRECIP.value,
            Columns.TEMP.value,
            Columns.HUM.value
        ])

    data_record_df1[Columns.MEASURED_AT.value] = pd.to_datetime(
        data_record_df1[Columns.AT.value])

    data_record_df1.drop(columns=[Columns.MEASUREMENTS.value], inplace=True)
    data_record_df1.drop(columns=[Columns.AT.value], inplace=True)

    def get_val(x): return x[Columns.VALUE.value]
    data_record_df2[Columns.PRECIP.value] = \
        data_record_df2[Columns.PRECIP.value].apply(get_val)
    data_record_df2[Columns.TEMP.value] = \
        data_record_df2[Columns.TEMP.value].apply(get_val)
    data_record_df2[Columns.HUM.value] = \
        data_record_df2[Columns.HUM.value].apply(get_val)

    data_record_df3 = pd.concat([data_record_df1, data_record_df2], axis=1)

    nested_data_records = data_record_df3.apply(
        lambda m: [
            {
                Columns.DATALOGGER.value: m[Columns.DATALOGGER.value],
                Columns.MEASURED_AT.value: m[Columns.MEASURED_AT.value],
                Columns.LABEL.value: Columns.PRECIP.value,
                Columns.VALUE.value: m[Columns.PRECIP.value]
            },
            {
                Columns.DATALOGGER.value: m[Columns.DATALOGGER.value],
                Columns.MEASURED_AT.value: m[Columns.MEASURED_AT.value],
                Columns.LABEL.value: Columns.TEMP.value,
                Columns.VALUE.value: m[Columns.TEMP.value]
            },
            {
                Columns.DATALOGGER.value: m[Columns.DATALOGGER.value],
                Columns.MEASURED_AT.value: m[Columns.MEASURED_AT.value],
                Columns.LABEL.value: Columns.HUM.value,
                Columns.VALUE.value: m[Columns.HUM.value]
            }
        ],
        axis=1,
    ).to_list()

    data_records_df = pd.DataFrame([
        data_record for data_record_list in nested_data_records
        for data_record in data_record_list
    ]).dropna()

    return data_records_df


def summarize_mean_by_span(data_records: pd.DataFrame, span: str) -> pd.DataFrame:
    data_records[Columns.MEASURED_AT.value] = pd\
        .to_datetime(data_records[Columns.MEASURED_AT.value])

    data_records[Columns.TIME_SLOT.value] = data_records[Columns.MEASURED_AT.value]\
        .dt.floor(TIME_SPANS[span])

    data_records[Columns.TIME_SLOT.value] = data_records[Columns.TIME_SLOT.value]\
        .apply(lambda t: pd.Timestamp(t).isoformat())

    grouped_data_records = data_records\
        .groupby([Columns.TIME_SLOT.value, Columns.LABEL.value])

    agg_df = grouped_data_records\
        .agg({Columns.VALUE.value: 'mean'})\
        .reset_index()
    return agg_df
