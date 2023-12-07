from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse




router = APIRouter()





async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


# this is streaming test api
@router.get("/")
async def main():

    some_file_path = "/code/backend/server/weather.mp4"
    def iterfile():  #
        chunk_size = 1024
        with open(some_file_path, mode="rb") as file_like:  #
            while True:
                chunk = file_like.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(iterfile())