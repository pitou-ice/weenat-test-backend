from pydantic import BaseModel


class DataRecordAggregateResponse(BaseModel):
    label: str
    time_slot: str
    value: float
