from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse




router = APIRouter()







# this is streaming test api
@router.get("/")
async def main():

    some_file_path = "/code/backend/server/weather.mp4"
    def iterfile():  #
        chunk_size = 1024 * 32
        with open(some_file_path, mode="rb") as stream_fd:  #
            while True:
                chunk = stream_fd.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(iterfile())