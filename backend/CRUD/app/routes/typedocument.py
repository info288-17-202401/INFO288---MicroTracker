# from typing import Any, Optional, List
# from databases.db import engine
# from sqlalchemy.orm import sessionmaker
# from fastapi import APIRouter, HTTPException

# from databases.serialized_models import TypeDocumentSerialized
# from databases.models import TypeDocument

# router = APIRouter()

# @router.get("/", response_model=List[TypeDocumentSerialized], status_code=200)
# def get_type_documents() -> Any:
#     """
#     Retrieve items.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         typedocument = session.query(TypeDocument).all()
#     finally:
#         session.close()
#     return typedocument


# @router.get("/{id}", response_model=TypeDocumentSerialized, status_code=200)
# def get_type_document(id: int) -> Any:
#     """
#     Get item by ID.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         typedocument = session.get(TypeDocument, TypeDocument._type)
#     finally:
#         session.close()
#     if not typedocument:
#         raise HTTPException(status_code=404, detail="Document not found")
#     return typedocument
