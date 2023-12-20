from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, field_validator, BaseConfig



class BasicSchema(BaseModel):
    name : str
    login_id : str

    class Config(BaseConfig):
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "name": "foobar",
                    "login_id" : "aaa1234",

                }
            ]
        }

class BaseUser(BasicSchema):
    password : str


class UserSchema(BasicSchema):
    password : str

    @field_validator('name',mode = 'before')
    @classmethod
    def check_nameform(cls, v: str):
        # 대문자 및 특수문자 존재여부
        if isinstance(v, str):
            if len(v) < 3:
                raise ValueError('이름은 세글자 이상만 가능합니다.')
        return v

    @field_validator('login_id',mode='before')
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

# class UserSchema(BaseUser):
#     password: Optional[str]
#
#
#     class Config(BaseConfig):
#         from_attributes = True
#         json_schema_extra = {
#             "examples": [
#                 {
#                     "name": "foobar",
#                     "login_id" : "aaa1234",
#                     "password" : "12345678"
#
#                 }
#             ]
#         }