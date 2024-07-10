import os
import uvicorn
import logging
from typing import Final
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from routers import data_record
from core.database import engine
from models.data_record import DataRecordORM
from core.constants import DEFAULT_HOST, DEFAULT_PORT, MAIN_APP


logger = logging.getLogger(__name__)


load_dotenv()
UVICORN_HOST: Final[str] = os.getenv('UVICORN_HOST', DEFAULT_HOST)
UVICORN_PORT: Final[int] = int(os.getenv('UVICORN_PORT', DEFAULT_PORT))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Creating database tables.')
    DataRecordORM.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(data_record.router)


if __name__ == '__main__':
    uvicorn.run(
        MAIN_APP,
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=True  # TODO remove this line
    )
