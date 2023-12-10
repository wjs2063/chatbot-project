from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from schema.item import UserSchema
from model.item import UserModel
from db.session import get_db
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/sign-up")
async def create_user(user:UserSchema,db : AsyncSession = Depends(get_db)):

    # check if user exists
    stmt = select(UserModel).where(UserModel.user_id == user.user_id).limit(1)
    result = await db.execute(stmt)
    result = result.scalars().first()
    if result:
        return {"msg" : "이미 가입된 회원입니다. 회원찾기를 이용해주세요"}
    # sign-up
    user_model = UserModel(name=user.name,user_id=user.user_id,password=user.user_password)
    try:
        db.add(user_model)
        await db.commit()
    except Exception as e :
        await db.rollback()
        print(e)
        return {"msg" : "현재 회원가입이 불가능합니다. 관리자에게 문의해주세요"}
    return {"msg" : f"{user_model.name} 회원가입 성공"}

@router.get("/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": 1}

