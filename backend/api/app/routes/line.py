from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import SessionLocal
# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException

from app.models.serialized_models import (LineSerialized,MicrobusSerialized) #Como retorna la api
from app.models.models import (Line, Microbus) #Obtiene desde la BD

#READY agregar ruta al modelo sql
router = APIRouter()
@router.get("/", response_model=List[LineSerialized], status_code=200)
def get_lines() -> Any:
    """
    Get all the lines.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        line = session.query(Line).all()
        # return line
    except Exception as e:
        raise HTTPException(status_code=404, msg="Can't connect to databases", detail=e)
    finally:
        session.close()
    return line
    
#Lugares por donde pasa la linea
@router.get("/{id}", response_model=LineSerialized, status_code=200)
def get_line(id: int) -> Any:
    """
    Get line by ID.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        line = session.get(Line, id)
        if not line:
            raise HTTPException(status_code=404, detail="Item not found")
        return line
    finally:
        session.close()

@router.post("/", response_model=Any, status_code=201)
def create_line(line: LineSerialized) -> Any:
    """
    Get item by ID.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        line = session.add(Line(
            number = line.number,
            color = line.color,
        ))
        session.commit()
        
        return {"ok": True, "status":201, "detail": "Line added", "line": line} 
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add line \n {str(e)}")
    finally:
        session.close()