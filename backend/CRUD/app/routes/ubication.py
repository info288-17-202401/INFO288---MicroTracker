# from typing import (Any, 
#                     # Optional, 
#                     List)
# from app.core.conexion_db import engine
# from sqlalchemy.orm import sessionmaker
# from fastapi import APIRouter, HTTPException

# from app.models.serialized_models import UbicationSerialized #Como retorna la api
# from app.models.models import Ubication #Obtiene desde la BD

# router = APIRouter()
# @router.get("/", response_model=List[UbicationSerialized], status_code=200)
# def get_ubications() -> Any:
#     """
#     Retrieve items.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         ubication = session.query(Ubication).all()
#         # return ubication
#     except Exception as e:
#         raise HTTPException(status_code=404, detail="Can't connect to databases")
#     finally:
#         session.close()
#     return ubication
    

# @router.get("/{id}", response_model=UbicationSerialized, status_code=200)
# def get_ubication(id: int) -> Any:
#     """
#     Get item by ID.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         ubication = session.get(Ubication, id)
#         if not ubication:
#             raise HTTPException(status_code=404, detail="Item not found")
#         return ubication
#     finally:
#         session.close()
    