from fastapi import APIRouter

from .container import Container
from . import endpoints


def create_router() -> APIRouter:
    container = Container()
    router = APIRouter()
    router.container = container
    router.include_router(endpoints.router)
    return router

router = create_router()