from pydantic import BaseModel, field_validator, BaseConfig
from typing import Optional

class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ItemScheme(ItemBase):
    pass