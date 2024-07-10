from sqlalchemy import select
from sqlalchemy.orm import Session

from models.data_record import DataRecordORM


def add_all_data_records(
    data_records_dicts: list[dict],
    db: Session
) -> None:
    data_records = [
        DataRecordORM(**data_record)
        for data_record
        in data_records_dicts
    ]

    db.add_all(data_records)
    db.commit()


def select_data_records_by_datalogger_in_timeframe(
    datalogger: str,
    db: Session,
    since: str | None = None,
    before: str | None = None
) -> list[dict]:
    query = select(DataRecordORM)\
        .where(DataRecordORM.datalogger == datalogger)\
        .where(DataRecordORM.measured_at.between(since, before))
    data_records = db.execute(query).scalars().all()

    return data_records
