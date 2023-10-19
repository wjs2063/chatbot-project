"""
schema.py
return schema
"""
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel



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

