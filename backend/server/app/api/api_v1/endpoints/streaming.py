from fastapi import APIRouter, Depends, Request, Header, HTTPException, status
from fastapi.responses import StreamingResponse
from pathlib import Path
from components.stream import stream_file, download_handler
import os

router = APIRouter()


# this is streaming test api

@router.post("/download", summary="비디오 다운로드")
async def video_download(video_id: str):
    res = await download_handler.download(video_id)
    if res == 0:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED)
    return {"msg": "다운로드 완료"}


@router.get("/{video_id}", summary="비디오 스트리밍")
async def streaming(video_id: str, range: str = Header()):
    try:
        file_list = os.listdir(f"/code/backend/server/{video_id}")
        video_file_path = Path(f"/code/backend/server/{video_id}/{file_list[0]}")
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
        media_type="video/mp4",
        headers={
            'Accept-Ranges': 'bytes',
            'Content-Range': f'bytes {start}-{end}/{file_byte_size}',
            'Content-Length': str(content_length),
        }
    )
