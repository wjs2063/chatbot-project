import asyncio

from meta.common import SingletonMeta
import os
from pytube import YouTube
from ArtificalIntelligence.constant import yt_baseurl
from core.constant import audio_base_path


def stream_file(start, end,video_file_path):
    with open(video_file_path, mode="rb") as file_bytes:
        file_bytes.seek(start)
        stream_chunk = file_bytes.read(end - start)
        yield stream_chunk

class DownloadHandler(metaclass=SingletonMeta):
    def __init__(self):
        self.base_path = audio_base_path
        pass

    async def download(self,video_id):
        dir_path = f"{self.base_path}/{video_id}/"
        if os.path.isdir(dir_path):return 0
        download_path = dir_path + video_id + ".mp4"
        os.makedirs(os.path.dirname(dir_path), exist_ok=True)
        yt = YouTube(f"{yt_baseurl}?v={video_id}")
        yt.captions.all()
        video = yt.streams.filter(file_extension='mp4').first()
        await asyncio.to_thread(video.download,dir_path)
        return 1

download_handler = DownloadHandler()