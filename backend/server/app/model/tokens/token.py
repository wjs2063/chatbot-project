from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from asyncio import run

class RefreshToken(Base):
    __tablename__ = "refreshtoken"
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    name = Column(String,index=True)
    token = Column(String)
    create_time = Column(DateTime)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r}, token:{self.token!r}, create_time:{self.create_time!r}"