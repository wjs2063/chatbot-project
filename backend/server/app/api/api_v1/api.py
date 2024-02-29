from fastapi import APIRouter
from api.api_v1.endpoints import llms, auth, crud_test
from containers.stream_container.application import router as stream_router
from containers.summarize_container.application import router as summarize_router

api_router = APIRouter()

api_router.include_router(llms.router, prefix="/llms", tags=["llms"])
# api_router.include_router(streaming.router, prefix="/streaming", tags=["streaming"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(crud_test.router, prefix="/db_test", tags=["database"])
api_router.include_router(stream_router, prefix="/streaming", tags=["streaming"])
api_router.include_router(summarize_router, prefix="/summarize", tags=["summarize"])
