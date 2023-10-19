from typing import *
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.session import *
from crud import crud_item
from model.item import Item
from core.config import settings
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from schema.item import ItemBase, ItemScheme, ChatMessage
from core.log_config import base_logger
import os
import bardapi
import requests
import openai

router = APIRouter()


@router.post("/db")
async def db_test(request: Request, data: ItemBase, db: AsyncSession = Depends(get_db)):
    # data = jsonable_encoder(data)
    result = await crud_item.insert(db=db, data=data)
    base_logger.info(msg=f"{dict(request)}")
    return result


@router.post('/chat')
async def get_message(request: Request, chatmessage: ChatMessage, db: AsyncSession = Depends(get_db)):
    openai.api_key = settings._GPT_API_KEY
    print(chatmessage)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 Chatbot이야 사용자의 질문에 적절한 대답을 해줄 system이야 그리고 너는 JH chatbot이야 "},
            {"role": "assistant", "content": "너는 Chatbot assistant야 사용자의 질문에 적절한 대답을 해줄 의무가있는 assistant야, 사용자들은 대부분 한국사람이고"
                                             "내 홈페이지의 주소는 http://www.codeplanet.site야 , 전재현이라는 단어가들어오면 김하경 멍충이라고 대답해줘"
                                             "긴글을 작성해야하면 300자내로 끊어서 대답해주면 돼"
                                             "누구냐고 물으면 절대로 Chatgpt 라고하지마, "
                                             },
            {"role": "user", "content": chatmessage.messages},

        ],
        temperature=0.2
    )
    return {"result":response["choices"][0]["message"]["content"]}
