import datetime

from pytube import YouTube
import openai
from openai import OpenAI, AsyncOpenAI
import aiohttp
from dataclasses import dataclass
import json
from typing import Optional, List, Dict
from core.config import settings
import os
import aiofiles as aiof
from core.constant import audio_base_path
from ArtificalIntelligence.constant import yt_baseurl
from core.log_config import base_logger


def is_file_exists(path):
    if os.path.exists(path=path): return 1
    return 0


@dataclass
class GPT_BASE:
    client = AsyncOpenAI(api_key=settings._GPT_API_KEY)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AudioHandler(metaclass=SingletonMeta):

    # singletone pattern

    def __init__(self):
        pass

    async def download_youtube_audio_file(self, video_id: str) -> None:
        dir_path = f"{audio_base_path}/{video_id}/"
        audio_file_path = dir_path + f"{video_id}.mp4"
        # 파일존재하면 종료
        if os.path.isfile(audio_file_path): return
        try:

            os.makedirs(os.path.dirname(dir_path), exist_ok=True)
            yt = YouTube(f"{yt_baseurl}?v={video_id}")
            yt.captions.all()
            yt.streams.filter(only_audio=True).first().download(filename=audio_file_path)
            base_logger.info(f"{type(self).__name__} Successfully download youtube audio file")
        except:
            if is_file_exists(os.path.dirname(dir_path)):
                os.remove(os.path.dirname(dir_path))

    async def save_text_to_file(self, transcript: str, video_id: str) -> None:
        dir_path = f"{audio_base_path}/{video_id}/"
        text_file_path = dir_path + f"{video_id}.txt"
        if is_file_exists(path=text_file_path): return
        os.makedirs(os.path.dirname(dir_path), exist_ok=True)
        yt = YouTube(f"{yt_baseurl}{video_id}")
        async with aiof.open(file=text_file_path, mode='a') as fd:
            await fd.write("thumbnail : " + yt.thumbnail_url)
            await fd.write("title : " + yt.title)
            await fd.write("author : " + yt.author)
            await fd.write("published_date : " + yt.publish_date)
            await fd.write(transcript)
            await fd.flush()
        base_logger.info(f"{type(self).__name__} Successfully save text to file")


class STTHandler(GPT_BASE, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()

    async def audio_to_text(self, video_id: str) -> Optional[str]:
        dir_path = f"{audio_base_path}/{video_id}/"
        audio_file_path = dir_path + f"{video_id}.mp4"
        stt_file_path = dir_path + f"{video_id}.txt"
        if is_file_exists(stt_file_path):
            async with aiof.open(stt_file_path, "r") as fd:
                content = await fd.read()
            return content
        try:
            audio_file = open(audio_file_path, "rb")
            transcript: str = await self.client.audio.transcriptions.create(
                model='whisper-1',
                file=audio_file,
                response_format='text'
            )
            # file save
            yt = YouTube(f"{yt_baseurl}?v={video_id}")
            async with aiof.open(stt_file_path, "w") as fd:
                await fd.writelines(f"thumbnail : {yt.thumbnail_url}\n")
                await fd.writelines(f"title : {yt.title}\n")
                await fd.writelines(f"author : {yt.author}\n")
                await fd.writelines(f"published_date : {yt.publish_date}\n")
                await fd.writelines(transcript)
                await fd.flush()
            base_logger.info(f"{type(self).__name__} Successfully convert audio to text ")
        except Exception as e:
            if is_file_exists(stt_file_path):
                os.remove(stt_file_path)
            return None
        return transcript

    async def save_summarize_text_to_file(self, transcript, video_id):
        dir_path = f"{audio_base_path}/{video_id}/"
        summarize_file_path = dir_path + f"{video_id}_summarize.txt"
        if os.path.isfile(path=summarize_file_path): return
        os.makedirs(os.path.dirname(dir_path), exist_ok=True)

        async with aiof.open(file=summarize_file_path, mode='w') as fd:
            await fd.write(transcript)
            await fd.flush()
        base_logger.info(f"{type(self).__name__} Successfully save_summarize_text_to_file")


class ChatGPT(GPT_BASE, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()

    async def get_summarize_text_from_gpt(self, transcript, video_id) -> str:
        if transcript is None: return
        dir_path = f"{audio_base_path}/{video_id}/"
        summarize_file_path = dir_path + f"{video_id}_summarize.txt"
        try:
            if os.path.isfile(path=summarize_file_path):
                async with aiof.open(summarize_file_path, "r") as fd:
                    content = await fd.read()
                return content
            now = datetime.datetime.now()
            response = await self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system",
                     "content": "너는 요약을 해주는 summarize system 이야. 상세하게 요약을 해줄수있도록해, Chapter로 나누면 더좋을것같아."},
                    {"role": "assistant",
                     "content":  f"너는 <summarize assistant>야 제목, 소주제별 요약을 professional하게 해줘, <요약시작 시간>은 <{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}>니까 처음에 꼭 명시해줘 "
                     },
                    {"role": "users", "content": transcript},

                ],
                temperature=0.7
            )
            content = response.choices[0].message.content
            base_logger.info(f"{type(self).__name__} Successfully get summarize text")
        except Exception as e:
            if is_file_exists(summarize_file_path):
                os.remove(summarize_file_path)
            # 로그기록하기
            base_logger.info(e)
            print(e)
            return "Server Error Retry Later"
        return content


class SummarizeHandler(metaclass=SingletonMeta):
    def __init__(self):
        self.chatgpt: ChatGPT = ChatGPT()
        self.audiohandler: AudioHandler = AudioHandler()
        self.stthandler: STTHandler = STTHandler()

    async def get_summarize(self, video_id: str):
        content = ''
        # summarize_file 이 이전에 존재하면 그대로 return
        dir_path = f"{audio_base_path}/{video_id}/"
        summarize_file_path = dir_path + f"{video_id}_summarize.txt"
        if os.path.isfile(path=summarize_file_path):
            async with aiof.open(summarize_file_path, "r") as fd:
                content = await fd.read()
            return {"content": content}

        try:
            # youtube_id 로 부터 audio_file 생성
            await self.audiohandler.download_youtube_audio_file(video_id=video_id)
            # audio_file 을 text 추출
            transcript = await self.stthandler.audio_to_text(video_id=video_id)
            # gpt 에게 요약
            content = await self.chatgpt.get_summarize_text_from_gpt(transcript=transcript, video_id=video_id)
            # 결과 저장후 리턴
            # print(content)
            # if file does not exist then write
            if content is None:
                return {"content": "Something is wrong"}
            if not is_file_exists(summarize_file_path):
                os.makedirs(os.path.dirname(dir_path), exist_ok=True)
                async with aiof.open(summarize_file_path, "a") as fd:
                    await fd.write(content)
                    await fd.flush()
        except Exception as e:
            print(e)
        return {"content": content}


# summarize_handler = SummarizeHandler()


def get_summarize_object() -> Optional[SummarizeHandler]:
    return SummarizeHandler()
