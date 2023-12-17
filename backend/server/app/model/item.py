"""
model.py -> database schema
"""

from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base
from asyncio import run
from db.session import *



class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String, index=True)
    description = Column(String)


    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, title={self.title!r}, description={self.description!r})"

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    name = Column(String)
    login_id = Column(String,index=True,unique=True)
    password = Column(String)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r}, user_id={self.login_id!r}), password = secret!!"