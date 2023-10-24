from typing import *
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.session import *
from crud import crud_item
from core.config import settings
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from schema.item import ItemBase, ItemScheme, ChatMessage
from core.log_config import base_logger
import os
from crud.crud_item import *
import requests
import openai
import re
from schema.item import WitResponse
router = APIRouter()
print(os.getcwd())

@router.post("/db")
async def db_test(request: Request, data: ItemBase, db: AsyncSession = Depends(get_db)):
    # data = jsonable_encoder(data)
    result = await crud_item.insert(db=db, data=data)
    base_logger.info(msg=f"{dict(request)}")
    return result

@router.post("/test/redis")
async def test_redis(request:Request,msg : str,redis = Depends(get_redis)):
    value = await redis.get(msg)
    print(value)
    redis_response = await redis.set("test","hello")
    return {"result":value}


@router.post('/chat')
async def get_message(request: Request, chatmessage: ChatMessage, db: AsyncSession = Depends(get_db),redis = Depends(get_redis)):
    # get response from witai
    wit_response = get_witai_nlu_response(chatmessage)
   #print(wit_response.json())
    wit : WitResponse = WitResponse(response=wit_response,status=400)
    wit_intent = wit.get_intent()
    wit_confidence = wit.get_confidence()

    #print(f"intent : {wit_intent}, confidence : {wit_confidence}, wit_response : {wit.response}")
    if wit.status == 200 and wit_confidence > 0.95:
        wit_intent = wit.get_intent()

        # 만약 intent 가 redis 에 있다면 바로 반환 GPT 까지 갈필요 X
        value = await redis.get(wit_intent)
        if value is not None:
            #print("cache value : ", value.decode('utf-8'))
            return {"result": value}

    openai.api_key = settings._GPT_API_KEY
    #print(chatmessage)
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 Chatbot이야 사용자의 질문에 적절한 대답을 해줄 system이야 그리고 너의 이름은 콩돌이 Chatbot이야"
                                          "답변은 300자내로 끊어서 대답해주면 돼"},
            {"role": "assistant", "content": "너는 Chatbot assistant야 사용자의 질문에 적절한 대답을 해줄 의무가있는 assistant야, 사용자들은 대부분 한국사람이고"
                                             "이 홈페이지의 주소는 http://www.codeplanet.site야 "
                                             "누구냐고 물으면 절대로 Chatgpt 라고하지마, "
                                             },
            {"role": "user", "content": chatmessage.messages},

        ],
        temperature=0.2
    )
    response_str = response["choices"][0]["message"]["content"]
    response_str = re.sub("gpt | GPT | OpenAI | openai | chatgpt", "", response_str)
    if wit_confidence > 0.95:
        await redis.set(wit_intent,response_str)
    return {"result": response_str}
