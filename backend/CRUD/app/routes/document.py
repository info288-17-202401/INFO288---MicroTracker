# from typing import Any, Optional, List, Dict
# from databases.db import engine
# from sqlalchemy.orm import sessionmaker
# from fastapi import APIRouter, HTTPException, Query
# from databases.serialized_models import DocumentSerialized, DocumentSerializedRequired
# from databases.models import Document, TypeDocument
# from sqlalchemy import func

# router = APIRouter()

# @router.get("/", response_model=List[DocumentSerialized], status_code=200)
# def get_documents(title: str | None = Query(None), _type:str | None = Query(None)) -> Any:
#     """
#     Retrieve documents.
#     """
#     documents = []
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         if title and _type:
#             # print("Title:", title)
#             # print("Type:", _type)
#             documents = session.query(Document).join(TypeDocument, Document.type_document_id == TypeDocument._type).filter(func.lower(Document.title).ilike(f"%{title.lower()}%")).filter(func.lower(TypeDocument._type).ilike(f"%{_type.lower()}%"))
#         elif title:
#             # print("Title:", title)
#             for title in title.split(" "):
#                 documents_ = session.query(Document).filter(Document.title.ilike(f"%{title.lower()}%")).all()
#                 if documents_: 
#                     documents.extend(documents_)
#                 print(documents_)

#         elif _type:
#             # print("Type:", _type)
#             documents = session.query(Document).filter(TypeDocument._type.ilike(_type)).all()

#         else:
#             documents = session.query(Document).all()
#     except Exception as e:
#         print(e)
#     finally:
#         session.close()

#     return documents

# @router.get("/{id}", response_model=DocumentSerialized, status_code=200)
# def get_document(id: int) -> Any:
#     """
#     Get document by ID.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         document = session.get(Document, id)
#     finally:
#         session.close()
#     if not document:
#         raise HTTPException(status_code=404, detail="Document not found")
#     return document

# @router.post("/", status_code=201, response_model=Any)
# def post_document(document: DocumentSerializedRequired) -> Any:
#     """
#     Retrieve documents.
#     """
#     try: 
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         # document = Document(**body)
#         document = session.add(Document(title=document.title, publication_date=document.publication_date, type_document_id=document.type_document_id))
#         session.commit()
#         # return {"detail": "Document added"}
#         return {"ok": True, "status":201, "detail": "Document added"} 
    
#     except Exception as e:
#         print("Can't add document")
#         print(e)
#         raise HTTPException(status_code=500, detail="Can't add document")
#     finally:
#         session.close()
