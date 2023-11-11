from fastapi import FastAPI
from api.api_v1.api import api_router
from core.config import settings
import sqlalchemy
from db.session import get_db, engine
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import run
from db.session import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)

origins = [
    "http://localhost:3000",
    # "http://172.30.1.50:3000",
    "http://www.codeplanet.site",
    "http://www.codeplanet.site:50001",
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
    print("fastapi-server started!!")
    await create_tables(engine=engine, metadata=metadata)
    print("postgresql-tables created!!")


@app.on_event("shutdown")
async def shutdown():
    print("fastapi-server closed!!")


@app.get("/")
async def test():
    return "hello Welcome to fastapi"
