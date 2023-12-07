from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse




router = APIRouter()





async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


# this is streaming test api 
@router.get("/")
async def main():

    some_file_path = "/code/backend/server/Blue_Sky_and_Clouds_Timelapse_0892__Videvo.mp4"
    def iterfile():  #
        with open(some_file_path, mode="rb") as file_like:  #
            yield from file_like  #

    return StreamingResponse(iterfile())