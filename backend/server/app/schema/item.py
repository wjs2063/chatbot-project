"""
schema.py
return schema
"""
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel, field_validator, BaseConfig
from typing import Dict, List, Optional, Union
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
    messages: str


@dataclass
class RedisHandler():
    pass


class BaseUser(BaseModel):
    name: str
    login_id: str


class UserSchema(BaseUser):
    password: Optional[str]

    @field_validator('name')
    @classmethod
    def check_nameform(cls, v: str):
        # 대문자 및 특수문자 존재여부
        if isinstance(v, str):
            if len(v) < 3:
                raise ValueError('이름은 세글자 이상만 가능합니다.')
        return v

    @field_validator('login_id')
    @classmethod
    def check_nameform(cls, v: str):
        # 대문자 및 특수문자 존재여부
        if isinstance(v, str):
            if len(v) < 5:
                raise ValueError('아이디 길이는 5자이상만 가능합니다.')
        return v


    class Config(BaseConfig):
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "name": "foobar",
                    "login_id" : "aaa1234",
                    "password" : "12345678"

                }
            ]
        }


# class LoginForm(BaseModel):
#     user_id : str
#     user_password : str
#
#     @field_validator('user_password')
#     @classmethod
#     def check_password(cls,v:str):
#         if isinstance(v,str):
#             if len(v) < 8:
#                 raise ValueError('비밀번호는 8자이상만 가능합니다.')
#         return v
#
#     class Config:
#         from_attributes = True


print("model.item class is created!")
