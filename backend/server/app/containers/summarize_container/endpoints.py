from fastapi import APIRouter, Request, Depends
from dependency_injector.wiring import inject, Provide
from .container import Container

router = APIRouter()


@router.post("/summarize-video", summary="유튜브 비디오 요약")
@inject
async def get_summarize(request: Request, video_id: str,
                        summarize_service=Depends(Provide[Container.summarize_service])):
    response = await summarize_service.get_summarize(video_id=video_id)
    return response
