from fastapi import APIRouter

from . import   (microbus, 
                    # document, 
                    typedocument
                )

api_router = APIRouter()

api_router.include_router(microbus.router, prefix="/microbus", tags=["microbus"])
# api_router.include_router(author.router, prefix="/authors", tags=["authors"])
# api_router.include_router(document.router, prefix="/documents", tags=["documents"])
