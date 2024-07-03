from enum import Enum


class Columns(Enum):
    DATALOGGER = 'datalogger'
    MEASURED_AT = 'measured_at'
    TIME_SLOT = 'time_slot'
    LABEL = 'label'
    VALUE = 'value'
    AT = 'at'
    MEASUREMENTS = 'measurements'
    PRECIP = 'precip'
    TEMP = 'temp'
    HUM = 'hum'


class Tables(Enum):
    DATA_RECORD = 'data_record'
