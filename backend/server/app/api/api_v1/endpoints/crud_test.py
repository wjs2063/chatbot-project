from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, APIRouter,HTTPException
from schema.users.user import UserSchema
from schema.items.item import ItemBase
from model.users.user import UserModel
from model.items.item import Item
from model.videos.video import Video
from schema.videos.video import VideoSchema
from db.session import get_db


router = APIRouter()


@router.post("/create_db_detail",response_model = VideoSchema)
async def create_item(video : VideoSchema,db : AsyncSession = Depends(get_db)):
    vd_item = Video(
        name=video.name
    )
    try :
        db.add(vd_item)
        await db.commit()
    except:
        raise HTTPException(status_code=500,detail="cannot insert into database",headers={"X-ERROR" : "db_error"})
    return video

