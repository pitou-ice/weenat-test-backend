import os
from typing import Final
from dotenv import load_dotenv
from sqlalchemy import create_engine

from core.constants import DEFAULT_DATABASE


load_dotenv()
SQLALCHEMY_DATABASE_URL: Final[str] = os.getenv(
    'SQLALCHEMY_DATABASE_URL',
    DEFAULT_DATABASE
)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
