# from typing import (Any, 
#                     # Optional, 
#                     List)
# from app.core.conexion_db import engine
# from sqlalchemy.orm import sessionmaker
# from fastapi import APIRouter, HTTPException

# from app.models.serialized_models import LineSerialized #Como retorna la api
# from app.models.models import Line #Obtiene desde la BD

# router = APIRouter()
# @router.get("/", response_model=List[LineSerialized], status_code=200)
# def get_lines() -> Any:
#     """
#     Retrieve items.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         line = session.query(Line).all()
#         # return line
#     except Exception as e:
#         raise HTTPException(status_code=404, msg="Can't connect to databases", detail=e)
#     finally:
#         session.close()
#     return line
    

# @router.get("/{id}", response_model=LineSerialized, status_code=200)
# def get_line(id: int) -> Any:
#     """
#     Get item by ID.
#     """
#     try:
#         SessionLocal = sessionmaker(bind=engine)
#         session = SessionLocal()
#         line = session.get(Line, id)
#         if not line:
#             raise HTTPException(status_code=404, detail="Item not found")
#         return line
#     finally:
#         session.close()
    