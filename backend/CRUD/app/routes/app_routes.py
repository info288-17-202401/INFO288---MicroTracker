from fastapi import APIRouter

from . import   (
    microbus, 
    microbusstate     
    )

api_router = APIRouter()

api_router.include_router(microbus.router, prefix="/microbus", tags=["microbus"])
api_router.include_router(microbusstate.router, prefix="/microbusstate", tags=["microbusstate"])
# api_router.include_router(velocity.router, prefix="/velocity", tags=["velocity"])
# api_router.include_router(passenger.router, prefix="/passenger", tags=["passenger"])
