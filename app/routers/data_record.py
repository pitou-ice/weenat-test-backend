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


@router.get('/data', response_model=list[DataRecordResponse])
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

    return data_records.to_dict(orient='records')


@router.get('/summary', response_model=list[DataRecordResponse | DataRecordAggregateResponse])
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
    if span:
        data_records = summarize_mean_by_span(data_records, span)

    return data_records.to_dict(orient='records')
