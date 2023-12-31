from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, field_validator, BaseConfig



class BasicVideoSchema(BaseModel):
    name : str

    class Config(BaseConfig):
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "name" : "Triumph des Willens_1935"

                }
            ]
        }



class VideoSchema(BasicVideoSchema):

    @field_validator('name',mode='before')
    @classmethod
    def check_name(cls, v: str):
        # 대문자 및 특수문자 존재여부
        if isinstance(v, str):
            if len(v) < 1:
                raise ValueError('영화 이름은 공백이 불가능합니다.')
        return v

    class Config(BaseConfig):
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "name" : "Triumph des Willens_1935"

                }
            ]
        }

