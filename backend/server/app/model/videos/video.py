from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base
from asyncio import run

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    name = Column(String,unique=True)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, video_name={self.name!r})"
