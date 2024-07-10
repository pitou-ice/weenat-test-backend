from datetime import datetime
from pydantic import BaseModel


class DataRecordBase(BaseModel):
    label: str
    measured_at: datetime
    value: float


class DataRecordCreate(DataRecordBase):
    datalogger: str


class DataRecord(DataRecordBase):
    id: int

    class Config:
        from_attributes = True
