from sqlalchemy import Column, Integer, String, Float

from core.enums import Tables
from core.database import Base


class DataRecordORM(Base):
    __tablename__ = Tables.DATA_RECORDS.value

    id = Column(Integer, primary_key=True, index=True)
    datalogger = Column(String)
    label = Column(String)
    measured_at = Column(String)
    value = Column(Float)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
