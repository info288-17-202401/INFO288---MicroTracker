# from typing import Any, Optional, List
# from core.conexion_db import engine
# from sqlalchemy.orm import sessionmaker

# from fastapi import APIRouter, HTTPException

# from app.models.serialized_models import MicrobusSerialized
# from app.models.serialized_models import Microbus

# router = APIRouter()
# @router.get("/", response_model=List[MicrobusSerialized], status_code=200)
# def get_microbuses() -> Any:
#     """
#     Retrieve items.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         microbus = session.query(Microbus).all()
#     finally:
#         session.close()
#     return {
#         "ok": True,
#         "code": 200,
#         "detail": "Items has been retrieved successfully.",
#         "microbus": microbus
#     }
    


# @router.get("/{id}", response_model=MicrobusSerialized, status_code=200)
# def get_microbus(id: str) -> Any:
#     """
#     Get item by ID.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         microbus = session.get(Microbus, id)
#         if not microbus:
#             raise HTTPException(status_code=404, detail="Item not found")
#     finally:
#         session.close()
#     return {
#         "ok": True,
#         "code": 200,
#         "detail": "Items has been retrieved successfully.",
#         "microbus": microbus
#     }
    

