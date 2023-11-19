import os

from fastapi import FastAPI,Request
from api.api_v1.api import api_router
from core.config import settings
import time
import sqlalchemy
from db.session import get_db, engine
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import run
from db.session import *
from fastapi.middleware.cors import CORSMiddleware
from core.log_config import base_logger

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)

origins = [
    "http://localhost:3000",
    # "http://172.30.1.50:3000",
    "http://www.codeplanet.site",
    "http://www.codeplanet.site:50001",
    "http://www.codeplanet.site:9999"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    print("main_directory : ",os.getcwd())
    print("fastapi-server started!!")
    await create_tables(engine=engine, metadata=metadata)
    print("postgresql-tables created!!")


@app.on_event("shutdown")
async def shutdown():
    print("fastapi-server closed!!")

# add middle ware process_time header
@app.middleware('http')
async def add_process_time_header(request:Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def test():
    sle
    return "hello Welcome to fastapi"
