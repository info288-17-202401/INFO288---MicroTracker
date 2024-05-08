from fastapi import APIRouter

from . import   (
    microbus, 
    ubication, 
    velocity,
    passenger            
    )

api_router = APIRouter()

api_router.include_router(microbus.router, prefix="/microbus", tags=["microbus"])
api_router.include_router(ubication.router, prefix="/ubication", tags=["ubication"])
api_router.include_router(velocity.router, prefix="/velocity", tags=["velocity"])
api_router.include_router(passenger.router, prefix="/passenger", tags=["passenger"])
