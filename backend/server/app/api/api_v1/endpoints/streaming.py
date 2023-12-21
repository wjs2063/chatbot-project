from fastapi import APIRouter, Depends, Request,Header,HTTPException,status
from fastapi.responses import StreamingResponse
from pathlib import Path



router = APIRouter()







# this is streaming test api
@router.get("/")
async def streaming(range : str = Header()):
    video_file_path = Path("/code/backend/server/weather.mp4")
    file_byte_size = video_file_path.stat().st_size
    range_parts = range.replace('bytes=', '').split('-')
    start = int(range_parts[0])
    end = int(range_parts[1]) if len(range_parts) > 1 and range_parts[1] else file_byte_size - 1



    if start >= file_byte_size:
        raise HTTPException(status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

    end = min(end, file_byte_size - 1)
    content_length = end - start + 1

    def stream_file(start, end):
        with open(video_file_path, mode="rb") as file_bytes:
            file_bytes.seek(start)
            stream_chunk = file_bytes.read(end - start)
            yield stream_chunk


    return StreamingResponse(
        stream_file(start, end + 1),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type="video/mp4",
        headers={
            'Accept-Ranges': 'bytes',
            'Content-Range': f'bytes {start}-{end}/{file_byte_size}',
            'Content-Length': str(content_length),
        }
    )