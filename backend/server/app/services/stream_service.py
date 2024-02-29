from components.stream import stream_file
from fastapi.responses import StreamingResponse
from fastapi import Header, HTTPException, status
import mimetypes
import os
from pathlib import Path

class StreamService:

    async def stream_response(self,video_id,range):
        try:
            file_list = os.listdir(f"/code/backend/server/free-videos/{video_id}")
            file_list = [file for file in file_list if file.endswith(".mp4")]
            video_file_path = Path(f"/code/backend/server/free-videos/{video_id}/{file_list[0]}")
            media_type = mimetypes.guess_type(video_file_path)[0]
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