from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from core.enums import Tables
from core.database import engine


Base = declarative_base()


class DataRecordModel(Base):
    __tablename__ = Tables.DATA_RECORDS.value

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    datalogger: Mapped[str]
    measured_at: Mapped[str]
    label: Mapped[str]
    value: Mapped[float]


def create_data_records_table():
    Base.metadata.create_all(bind=engine)
