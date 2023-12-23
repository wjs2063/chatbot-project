from fastapi import APIRouter, Depends, Request, Header, HTTPException, status
from typing import List
from fastapi.responses import StreamingResponse
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from components.stream import stream_file, download_handler
from db.session import get_db
from crud.crud_item import crud
import mimetypes
import os
from model.videos.video import Video
from schema.videos.video import VideoSchema

router = APIRouter()


# this is streaming test api

@router.get("/movie-list", summary="비디오 리스트", response_model=List[VideoSchema])
async def get_video_list(page: int, db: AsyncSession = Depends(get_db)):
    response = await crud.get_video_list(db=db, page=3, last_seen=-1)
    return response


@router.post("/download", summary="비디오 다운로드")
async def video_download(video_id: str):
    res = await download_handler.download(video_id)
    if res == 0:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED)
    return {"msg": "다운로드 완료"}


# range: str = Header()
@router.get("/{video_id}", summary="비디오 스트리밍")
async def streaming(video_id: str, range: str = Header()):
    try:
        file_list = os.listdir(f"/code/backend/server/{video_id}")
        file_list = [file for file in file_list if file.endswith(".mp4")]
        print(file_list)
        video_file_path = Path(f"/code/backend/server/{video_id}/{file_list[0]}")
        media_type = mimetypes.guess_type(video_file_path)[0]
        print(media_type)
    except Exception as e:
        return {"msg": "파일 다운로드 요청을 해주세요"}
    file_byte_size = video_file_path.stat().st_size
    range_parts = range.replace('bytes=', '').split('-')
    start = int(range_parts[0])
    end = int(range_parts[1]) if len(range_parts) > 1 and range_parts[1] else file_byte_size - 1

    if start >= file_byte_size:
        raise HTTPException(status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

    end = min(end, file_byte_size - 1)
    content_length = end - start + 1

    return StreamingResponse(
        stream_file(start, end + 1, video_file_path=video_file_path),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type=media_type,
        headers={
            'Accept-Ranges': 'bytes',
            'Content-Range': f'bytes {start}-{end}/{file_byte_size}',
            'Content-Length': str(content_length),
        }
    )
