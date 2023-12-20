from fastapi import APIRouter
from api.api_v1.endpoints import llms, streaming, auth,crud_test

api_router = APIRouter()

api_router.include_router(llms.router, prefix="/llms", tags=["llms"])
api_router.include_router(streaming.router, prefix="/streaming", tags=["streaming"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(crud_test.router,prefix="/db_test",tags=["database"])

