from db.session import sessionLocal
import model.item as model
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
import requests
import aiohttp


async def insert(db: AsyncSession, data):
    item = model.Item(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


# 이후 비동기 함수로 변형
# async def get_witai_nlu_response(message):
#     witai_url = "https://api.wit.ai/message"
#     api_token = settings.WIT_AI_SERVER_TOKEN
#     params = {
#         "q": message
#     }
#     headers = {
#         "Authorization": f"Bearer {api_token}",
#     }
#     #response = requests.get(url=witai_url,params=params,headers=headers)
#     #print(response.json())
#     async with aiohttp.ClientSession() as session:
#         response = await session.get(url=witai_url,headers=headers, params=params)
#         print(await response.json())
#     return response
