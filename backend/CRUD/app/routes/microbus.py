from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
from fastapi import APIRouter, HTTPException

from app.models.serialized_models import MicrobusSerialized
from app.models.models import Microbus
# from app.core.Settings import settings

# Obtener el objeto logger para tu aplicación
router = APIRouter()
@router.get("/", response_model=List[MicrobusSerialized], status_code=200)
def get_microbuses() -> Any:
    """
    Retrieve items.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        microbus = session.query(Microbus).all()
        # return microbus
    except Exception as e:
        raise HTTPException(status_code=404, msg="Can't connect to databases", detail=e)
    finally:
        session.close()
    return microbus
    

@router.get("/{id}", response_model=MicrobusSerialized, status_code=200)
def get_microbus(id: str) -> Any:
    """
    Get item by ID.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        microbus = session.get(Microbus, id)
        if not microbus:
            raise HTTPException(status_code=404, detail="Item not found")
        return microbus
        
    finally:
        session.close()