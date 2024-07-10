from app.services import data_record
from app.schemas.data_record_request import DataRecordRequest
from app.schemas.data_record_response import DataRecordResponse

from test.mock import mock_request, mock_response, mock_response_aggregate_hour, mock_response_aggregate_day


def test_extract_data():
    data_record_requests = [
        DataRecordRequest(**raw_record)
        for raw_record
        in mock_request.data
    ]

    data_records = data_record.extract_data(data_record_requests)

    data_records = [
        DataRecordResponse.model_validate(clean_record).__dict__
        for clean_record
        in data_records
    ]

    assert data_records == mock_response.data


def test_aggregate_data_by_hour():
    data_records_aggregate = data_record.summarize_mean_by_span(
        mock_response.data, 'hour')

    assert data_records_aggregate == mock_response_aggregate_hour.data


def test_aggregate_data_by_day():
    data_records_aggregate = data_record.summarize_mean_by_span(
        mock_response.data, 'day')

    assert data_records_aggregate == mock_response_aggregate_day.data
