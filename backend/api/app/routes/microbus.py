from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
from fastapi import (APIRouter, 
                     HTTPException, 
                     Query)

from app.models.serialized_models import MicrobusSerialized
from app.models.models import Microbus
# from app.core.Settings import settings

# Obtener el objeto logger para tu aplicación
router = APIRouter()
@router.get("/", response_model=List[MicrobusSerialized], status_code=200)
def get_microbuses(id_line: int | None = Query(None)) -> Any:
    """
    Retrieve all microbuses from line, if there's no id line, get all the microbuses.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        if id_line:
            microbus = session.query(Microbus).filter(Microbus.line_id == id_line).all()
        else:
            microbus = session.query(Microbus).all()
        # return microbus
    except Exception as e:
        raise HTTPException(status_code=404, detail="Can't connect to databases")
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