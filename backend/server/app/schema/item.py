"""
schema.py
return schema
"""
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict,List,Optional,Union


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
class WitResponse():
    response : Optional[Dict] = None
    status : int = 400

    def __post_init__(self):
        try :
            self.status = self.response.status_code
            self.response = self.response.json()
        except Exception as e :
            print(e)
            self.response = dict()
            self.status = 400

    def get_intent(self) -> Union[None,int]:
        if self.response.get('intents') is None : return None
        if len(self.response['intents']) == 0 :return None
        return self.response['intents'][0]['name']
    def get_confidence(self) -> int :
        if self.response.get('intents') is None : return 0
        if len(self.response['intents']) == 0 : return 0
        return float(self.response['intents'][0]['confidence'])




@dataclass
class RedisHandler():
    pass



print("model.item class is created!")