from typing import Literal
from fastapi import APIRouter

from schemas.data_record_request import DataRecordRequest
from schemas.data_record_response import DataRecordResponse
from services.data_record import extract_data, summarize_mean_by_span
from schemas.data_record_aggregate_response import DataRecordAggregateResponse
from db.data_record import get_all_records_by_datalogger_in_datetime, append_data_records


router = APIRouter(
    prefix='/api',
    tags=['Data Records']
)


@router.post('/ingest')
async def create_data_records(data_records: list[DataRecordRequest]) -> dict:
    data_record_df = extract_data(data_records)
    append_data_records(data_record_df)
    return {}


@router.get('/data')
async def read_data(
    datalogger: str,
    since: str | None = None,
    before: str | None = None
) -> list[DataRecordResponse]:
    data_records = get_all_records_by_datalogger_in_datetime(
        datalogger,
        since,
        before
    )
    validated_data_records = [
        DataRecordResponse.model_validate(data_record)
        for data_record
        in data_records.to_dict('records')
    ]
    return validated_data_records


@router.get('/summary')
async def read_summary(
    datalogger: str,
    since: str | None = None,
    before: str | None = None,
    span: Literal['minute', 'hour', 'day'] | None = None
) -> list[DataRecordResponse | DataRecordAggregateResponse]:
    data_records = get_all_records_by_datalogger_in_datetime(
        datalogger,
        since,
        before
    )

    validation_model = DataRecordResponse
    if span:
        validation_model = DataRecordAggregateResponse
        data_records = summarize_mean_by_span(data_records, span)

    validated_data_records = [
        validation_model.model_validate(data_record)
        for data_record
        in data_records.to_dict('records')
    ]
    return validated_data_records
