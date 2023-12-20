from db.session import sessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Table, select
from core.config import settings
from core.log_config import SingletonMeta
from model.users.user import UserModel
from db.base import metadata
import requests
import aiohttp




class CRUD(metaclass=SingletonMeta):
    def __init__(self):
        pass

    async def insert(self, db, data):
        db.add(data)
        await db.commit()

    async def read(self, db, stmt):
        result = await db.execute(stmt)
        await db.commit()
        result = result.scalars()
        return result

    async def get_user(self,db,login_id):
        stmt = select(UserModel).where(UserModel.login_id == login_id).limit(1)
        response = await db.execute(stmt)
        await db.commit()
        result = response.scalars().first()
        return result



# async def insert(db: AsyncSession, data):
#     item = model.Item(**data.model_dump())
#     db.add(item)
#     await db.commit()
#     await db.refresh(item)
#     return item


crud = CRUD()
