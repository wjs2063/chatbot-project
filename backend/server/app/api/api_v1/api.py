from fastapi import APIRouter
from api.api_v1.endpoints import llms, streaming, authorization

api_router = APIRouter()

api_router.include_router(llms.router, prefix="/llms", tags=["llms"])
api_router.include_router(streaming.router, prefix="/streaming", tags=["streaming"])
api_router.include_router(authorization.router, prefix="/auth", tags=["authorzation"])


