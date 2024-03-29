from typing import *
from fastapi import APIRouter, Depends, Request, WebSocket
from db.session import *

from core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession

from schema.common import ChatMessage
from core.log_config import base_logger

from crud.crud_item import *

from openai import AsyncOpenAI
import re
from ArtificalIntelligence.witAI import WitAI, witai, WitResponse
from ArtificalIntelligence.summarize import get_summarize_object

router = APIRouter()


@router.post('/chat', summary="GPT 채팅")
async def get_message(request: Request, chatmessage: ChatMessage, db: AsyncSession = Depends(get_db),
                      redis=Depends(get_redis)):
    # get response from witai
    try:
        wit_response = await witai.get_response(chatmessage.messages)
        wit_response_json = await wit_response.json()
        wit: WitResponse = WitResponse(response=wit_response_json, status=wit_response.status)
        wit_intent = wit.get_intent()
        wit_confidence = wit.get_confidence()
        if wit.status == 200 and wit_confidence > 0.95:
            wit_intent = wit.get_intent()
            # 만약 intent 가 redis 에 있다면 바로 반환 GPT 까지 갈필요 X
            value = await redis.get(wit_intent)
            if value is not None:
                # print("cache value : ", value.decode('utf-8'))
                return {"result": value}

        gpt = AsyncOpenAI(api_key=settings._GPT_API_KEY)
        # print(chatmessage)
        response = await gpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "너는 GPT가 아닌 Chatbot이야 사용자의 질문에 적절한 대답을 해줄 system이야 그리고 너의 이름은 콩돌이 Chatbot이야"
                            "답변은 300자내로 끊어서 대답해주면 돼"},
                {"role": "assistant",
                 "content": "너는 <Chatbot assistant>야 사용자의 질문에 적절한 대답을 해줄 의무가있는 assistant야"
                 },
                {"role": "user", "content": chatmessage.messages},

            ],
            temperature=0.2
        )
        response_str = response.choices[0].message.content
        response_str = re.sub("gpt | GPT | OpenAI | openai | chatgpt", "", response_str)
        if wit_confidence > 0.95:
            await redis.set(wit_intent, response_str)
        return {"result": response_str}
    except Exception as e:
        print(e)
        return {"result": "retry next time"}


# @router.post("/summarize-video", summary="비디오 요약")
# async def get_summarize(request: Request, video_id: str, summarize_handler=Depends(get_summarize_object)):
#     response = await summarize_handler.get_summarize(video_id=video_id)
#     base_logger.info(response)
#     return response
@router.websocket("/chat/ws")
async def streaming_gpt(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive()
            async for text in streaming_gpt_response(message):
                await websocket.send(text)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


async def streaming_gpt_response(message):
    gpt = AsyncOpenAI(api_key=settings._GPT_API_KEY)
    response = await gpt.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "너는 GPT가 아닌 Chatbot이야 사용자의 질문에 적절한 대답을 해줄 system이야 그리고 너의 이름은 콩돌이 Chatbot이야"
                        "답변은 300자내로 끊어서 대답해주면 돼"},
            {"role": "assistant",
             "content": "너는 <Chatbot assistant>야 사용자의 질문에 적절한 대답을 해줄 의무가있는 assistant야"
             },
            {"role": "user", "content": message},

        ],
        temperature=0.2,
        stream=True
    )
    partial_content = ""
    async for chunk in response:
        content = chunk.choices[0].message.content
        if content is not None:
            partial_content += content
            yield partial_content
