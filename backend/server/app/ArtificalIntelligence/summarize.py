from pytube import YouTube
import openai
from openai import OpenAI
import aiohttp
from dataclasses import dataclass
import json
from typing import Optional,List,Dict
from core.config import settings
import os
import aiofiles as aiof
from core.constant import audio_base_path

def is_file_exists(path):
    if os.path.exists(path = path):return 1
    return 0

@dataclass
class GPT_BASE :
    client = OpenAI(api_key=settings._GPT_API_KEY)


class AudioHandler:
    def __init__(self):
        pass

    def download_youtube_audio_file(self,video_id:str) -> None :
        dir_path = f"{audio_base_path}/{video_id}/"
        audio_file_path = dir_path + f"{video_id}.mp4"
        if os.path.isfile(audio_file_path):return
        os.makedirs(os.path.dirname(dir_path), exist_ok=True)

        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        yt.streams.filter(only_audio=True).first().download(filename=audio_file_path)


    async def save_text_to_file(self,transcript:str, video_id:str) -> None :
        dir_path = f"{audio_base_path}/{video_id}/"
        text_file_path = dir_path + f"{video_id}.txt"
        if is_file_exists(path=text_file_path) : return
        os.makedirs(os.path.dirname(dir_path), exist_ok=True)

        async with aiof.open(file = text_file_path, mode = 'w') as fd:
            await fd.write(transcript)
            await fd.flush()
        print(f"audio to {video_id}.txt is done")

class STTHandler(GPT_BASE):
    def __init__(self):
        super().__init__()
    async def audio_to_text(self,video_id:str) -> Optional[str]:
        dir_path = f"{audio_base_path}/{video_id}/"
        audio_file_path = dir_path + f"{video_id}.mp4"
        stt_file_path = dir_path + f"{video_id}.txt"
        print("audio_file_path:",audio_file_path)
        print("stt_file_path:",stt_file_path)
        if is_file_exists(stt_file_path):
            async with aiof.open(stt_file_path, "r") as fd:
                content = await fd.read()
            return content
        audio_file = open(audio_file_path, "rb")
        transcript = self.client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            response_format='text'
        )
        print(transcript)
        # file save
        async with aiof.open(stt_file_path, "w") as fd:
            await fd.write(transcript)
            await fd.flush()
        return transcript


    async def save_summarize_text_to_file(self,transcript, video_id):
        dir_path = f"{audio_base_path}/{video_id}/"
        summarize_file_path = dir_path + f"{video_id}_summarize.txt"
        if os.path.isfile(path=summarize_file_path) : return
        os.makedirs(os.path.dirname(dir_path), exist_ok=True)

        async with aiof.open(file = summarize_file_path, mode = 'w') as fd:
            await fd.write(transcript)
            await fd.flush()
        print(f"audio to {video_id}.txt is saved")

class ChatGPT(GPT_BASE):
    def __init__(self):
        super().__init__()

    async def summarize_text(self,transcript):
        try :
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "너는 요약을 해주는 summarize system 이야. 상세하게 요약을 해줄수있도록해, Chapter로 나누면 더좋을것같아."},
                    {"role": "assistant",
                     "content": "너는 <summarize assistant>야 text에 적절한 요약을 professional하게 해줘"
                     },
                    {"role": "user", "content": transcript},

                ],
                temperature=0.7
            )
            content = response.choices[0].message.content
        except Exception as e :
            # 로그기록하기
            return {"result" : "Server Error Retry Later"}
        return content


class SummarizeHandler:
    def __init__(self):
        self.chatgpt : ChatGPT = ChatGPT()
        self.audiohandler : AudioHandler = AudioHandler()
        self.stthandler : STTHandler = STTHandler()

    async def get_summarize(self,video_id:str):

        # summarize_file 이 이전에 존재하면 그대로 return
        dir_path = f"{audio_base_path}/{video_id}/"
        summarize_file_path = dir_path + f"{video_id}_summarize.txt"
        if os.path.isfile(path=summarize_file_path) :
            async with aiof.open(summarize_file_path,"r") as fd:
                content = await fd.read()
            return {"content" : content}


        # youtube_id 로 부터 audio_file 생성
        self.audiohandler.download_youtube_audio_file(video_id=video_id)
        print("audio_handler 끝")
        # audio_file 을 text 추출
        transcript = await self.stthandler.audio_to_text(video_id=video_id)
        print("transcript 추출 완료",transcript)
        # gpt 에게 요약
        content = await self.chatgpt.summarize_text(transcript)
        print("gpt 요약 완료: ",content)
        # 결과 저장후 리턴

        os.makedirs(os.path.dirname(dir_path), exist_ok=True)
        async with aiof.open(summarize_file_path, "w") as fd:
            await fd.write(content)
            await fd.flush()
        print("파일저장 완료")

        return {"content" : content}

summarize_handler = SummarizeHandler()

class Summarize:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.chatgpt = ChatGPT()
            cls.audiohandler = AudioHandler()
            cls.stthandler = STTHandler()
        return cls.instance

def get_summarize_object() -> Optional[SummarizeHandler]:
    return Summarize()




