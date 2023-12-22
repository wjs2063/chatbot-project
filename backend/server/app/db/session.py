from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,AsyncEngine,async_sessionmaker
from core.config import settings
import sqlalchemy
from db.base import metadata,Base
from asyncio import run
import redis.asyncio as aioredis

engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

sessionLocal = async_sessionmaker(bind=engine,autocommit=False,class_=AsyncSession,autoflush=True,expire_on_commit=False)
#sessionLocal = AsyncSession(bind=engine)


async def create_tables(engine : AsyncSession,base:Base) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

async def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        await db.close()


#engine = AsyncEngine(create_engine(settings.ASYNC_SQLALCHEMY_DATABASE_URL,echo=True,future=True))
# Redis Connection
async def get_redis():
    redis_conn = await aioredis.from_url(f"redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}")
    try :
        yield redis_conn
    finally:
        await redis_conn.aclose()
print("DATABASE_SESSION LOADED!")