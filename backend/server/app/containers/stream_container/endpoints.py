
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Header, HTTPException, status
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from crud.crud_item import crud
from schema.videos.video import VideoSchema
from .container import Container

router = APIRouter()


# this is streaming test api

@router.get("/movie-list", summary="비디오 리스트", response_model=List[VideoSchema])
async def get_video_list(page: int, db: AsyncSession = Depends(get_db)):
    response = await crud.get_video_list(db=db, page=3, last_seen=-1)
    return response


@router.post("/download", summary="비디오 다운로드")
async def video_download(video_id: str, download_service=Depends(Provide[Container.download_service])):
    res = await download_service.download(video_id)
    if res == 0:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED)
    return {"msg": "다운로드 완료"}


# range: str = Header()
@router.get("/{video_id}", summary="비디오 스트리밍")
@inject
async def streaming(video_id: str, range: str = Header(), stream_service=Depends(Provide[Container.stream_service])):
    return await stream_service.stream_response(video_id=video_id, range=range)
