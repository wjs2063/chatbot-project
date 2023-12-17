from typing import Annotated,Union,Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from fastapi import Depends, APIRouter,Request,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schema.item import UserSchema,BaseUser
from model.item import UserModel
from db.session import get_db
from core.constant import ACCESS_TOKEN_EXPIRE_MINUTE
from crud.crud_item import crud
from security.auth import create_access_token,Token,get_current_user,get_hashed_password,verify_password

router = APIRouter()


@router.post("/sign-up")
async def create_user(user:UserSchema,db : AsyncSession = Depends(get_db)):

    # check if user exists
    result = await crud.get_user(db,login_id=user.login_id)
    if result:
        return {"msg" : "이미 가입된 회원입니다. 회원찾기를 이용해주세요"}
    # sign-up
    hashed_password = get_hashed_password(user.password)
    user_model = UserModel(name=user.name,login_id=user.login_id,password=hashed_password)
    try:
        db.add(user_model)
        await db.commit()
    except Exception as e :
        await db.rollback()
        print(e)
        return {"msg" : "현재 회원가입이 불가능합니다. 관리자에게 문의해주세요"}
    return {"msg" : f"{user_model.name} 회원가입 성공"}



@router.post('/token',response_model =Union[Token,Dict])
async def sign_in(request:Request,form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db : AsyncSession = Depends(get_db)):
    login_id = form_data.username
    result = await crud.get_user(db,login_id)
    if not result :
        raise HTTPException(status_code=400, detail="회원정보가 없습니다. 회원가입을 진행해주세요")
    plain_password = form_data.password
    if not verify_password(plain_password,result.password):
        raise HTTPException(status_code=400, detail="아이디 혹은 비밀번호가 일치하지않습니다. 다시 입력해주세요. ")
    # create_access_token
    data = {
        'sub' : form_data.username
    }
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    access_token = create_access_token(data=data,expires_delta=access_token_expires)


    return {"access_token" : access_token,"token_type" : "bearer"}


@router.get("/users/me",response_model = BaseUser)
async def read_items(current_user: BaseUser = Depends(get_current_user)):
    return current_user

