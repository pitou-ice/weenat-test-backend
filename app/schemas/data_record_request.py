from typing import Literal
from pydantic import BaseModel


class Measurement(BaseModel):
    label: Literal['precip', 'temp', 'hum']
    value: float | None


class DataRecordRequest(BaseModel):
    datalogger: str
    at: str
    measurements: list[Measurement]
