from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, APIRouter,HTTPException
from schema.item import UserSchema,ItemBase
from model.item import UserModel,Item
from db.session import get_db


router = APIRouter()


@router.post("/create_item")
async def create_item(item:ItemBase,db : AsyncSession = Depends(get_db)):
    db_item = Item(
        title=item.title,
        description=item.description
    )
    try :
        db.add(db_item)
        await db.commit()
    except:
        raise HTTPException(status_code=500,detail="cannot insert into database",headers={"X-ERROR" : "db_error"})
    return {"item" : item}

