from db.session import sessionLocal
import model.item as model
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

async def insert(db : AsyncSession, data):
    item = model.Item(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
