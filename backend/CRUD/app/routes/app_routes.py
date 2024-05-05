from fastapi import APIRouter

from . import   (
    microbus, 
    ubication, 
    line
                )

api_router = APIRouter()

api_router.include_router(microbus.router, prefix="/microbus", tags=["microbus"])
api_router.include_router(line.router, prefix="/line", tags=["line"])
# api_router.include_router(ubication.router, prefix="/ubication", tags=["ubication"])
