"""
schema.py
return schema
"""
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel,field_validator
from typing import Dict,List,Optional,Union
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import aiohttp
import re


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ItemScheme(ItemBase):
    pass


@dataclass
class ChatMessage(BaseModel):
    messages : str




@dataclass
class RedisHandler():
    pass

class UserSchema(BaseModel):
    name: str
    user_id : str
    user_password : str

    @field_validator('name')
    @classmethod
    def check_nameform(cls,v:str):
        # 대문자 및 특수문자 존재여부
        if isinstance(v, str):
            if len(v) < 3 :
                raise ValueError('이름은 세글자 이상만 가능합니다.')
        return v

    @field_validator('user_id')
    @classmethod
    def check_nameform(cls,v:str):
        # 대문자 및 특수문자 존재여부
        if isinstance(v, str):
            if len(v) < 8 :
                raise ValueError('아이디 길이는 8자이상만 가능합니다.')
        return v

    class Config:
        from_attributes = True


print("model.item class is created!")