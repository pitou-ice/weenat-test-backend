from typing import Literal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.database import get_db
from schemas.data_record_request import DataRecordRequest
from schemas.data_record_response import DataRecordResponse
from services.data_record import extract_data, summarize_mean_by_span
from schemas.data_record_aggregate_response import DataRecordAggregateResponse
from crud.data_record import add_all_data_records, select_data_records_by_datalogger_in_timeframe


router = APIRouter(
    prefix='/api',
    tags=['Data Records']
)


@router.post('/ingest')
async def post_ingest(
    data_record_requests: list[DataRecordRequest],
    db: Session = Depends(get_db)
) -> dict:
    data_records = extract_data(data_record_requests)
    add_all_data_records(data_records, db)

    return {}


@router.get('/data', response_model=list[DataRecordResponse])
async def get_data(
    datalogger: str,
    since: str | None = None,
    before: str | None = None,
    db: Session = Depends(get_db)
) -> list[DataRecordResponse]:
    data_records = select_data_records_by_datalogger_in_timeframe(
        datalogger=datalogger,
        since=since,
        before=before,
        db=db
    )

    return data_records


@router.get('/summary', response_model=list[DataRecordResponse | DataRecordAggregateResponse])
async def get_summary(
    datalogger: str,
    since: str | None = None,
    before: str | None = None,
    span: Literal['minute', 'hour', 'day'] | None = None,
    db: Session = Depends(get_db)
) -> list[DataRecordResponse | DataRecordAggregateResponse]:
    data_records = select_data_records_by_datalogger_in_timeframe(
        datalogger=datalogger,
        since=since,
        before=before,
        db=db
    )

    if span and data_records:
        data_records_dicts = [record.__dict__ for record in data_records]
        data_records = summarize_mean_by_span(data_records_dicts, span)

    return data_records
