from fastapi import APIRouter

from api.routes import author, document, typedocument

api_router = APIRouter()

# api_router.include_router(typedocument.router, prefix="/typedocument", tags=["typedocument"])
# api_router.include_router(author.router, prefix="/authors", tags=["authors"])
# api_router.include_router(document.router, prefix="/documents", tags=["documents"])
