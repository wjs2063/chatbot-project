from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,AsyncEngine
from core.config import settings
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from asyncio import run
import redis.asyncio as aioredis

engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

sessionLocal = sessionmaker(bind=engine,autocommit=False,class_=AsyncSession,autoflush=False)
#sessionLocal = AsyncSession(bind=engine)
Base = declarative_base()

metadata = Base.metadata

async def create_tables(engine : AsyncSession,metadata) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
print("redis connections is created!")