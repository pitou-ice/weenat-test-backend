import os
import uvicorn
from typing import Final
from fastapi import FastAPI
from dotenv import load_dotenv

from routers import data_record
from core.constants import DEFAULT_HOST, DEFAULT_PORT, MAIN_APP


load_dotenv()
UVICORN_HOST: Final[str] = os.getenv('UVICORN_HOST', DEFAULT_HOST)
UVICORN_PORT: Final[int] = int(os.getenv('UVICORN_PORT', DEFAULT_PORT))


app = FastAPI()
app.include_router(data_record.router)


if __name__ == '__main__':
    uvicorn.run(
        MAIN_APP,
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=True  # TODO remove this line
    )
