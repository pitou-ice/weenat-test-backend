from pydantic import BaseModel


class DataRecordResponse(BaseModel):
    label: str
    measured_at: str
    value: float
