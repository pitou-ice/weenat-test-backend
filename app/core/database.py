import os
from typing import Final
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()
SQLALCHEMY_DATABASE_URL: Final[str] = os.getenv(
    'SQLALCHEMY_DATABASE_URL', 'sqlite:///./database.sqlite')


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
