from dataclasses import dataclass
from core.config import settings
from schema.common import ChatMessage
from typing import Optional,Union,Dict
import aiohttp
from abc import ABCMeta,abstractmethod


class AIHandler:

    @abstractmethod
    async def get_response(self):
        pass



@dataclass
class WitAI(AIHandler):
    url : str
    response : Optional[Dict] = None
    status : int = 400

    # def __post_init__(self):
    #     try :
    #         self.status = self.response.status_code
    #         self.response =
    #     except Exception as e :
    #         print(e)
    #         self.response = dict()
    #         self.status = 400

    def __get_url(self):
        return self.url

    async def get_response(self,message:ChatMessage):
        witai_url = self.__get_url()
        api_token = settings.WIT_AI_SERVER_TOKEN
        params = {
            "q": message
        }
        headers = {
            "Authorization": f"Bearer {api_token}",
        }
        # response = requests.get(url=witai_url,params=params,headers=headers)
        # print(response.json())
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=witai_url, headers=headers, params=params)
        return response



witai = WitAI(url="https://api.wit.ai/message")


@dataclass
class WitResponse:
    response :Dict
    status :int = 500

    def get_intent(self) -> Union[None,int]:
        if self.response.get('intents') is None : return None
        if len(self.response['intents']) == 0 :return None
        return self.response['intents'][0]['name']
    def get_confidence(self) -> int :
        if self.response.get('intents') is None : return 0
        if len(self.response['intents']) == 0 : return 0
        return float(self.response['intents'][0]['confidence'])