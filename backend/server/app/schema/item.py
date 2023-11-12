"""
schema.py
return schema
"""
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict,List,Optional,Union
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import aiohttp

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



print("model.item class is created!")