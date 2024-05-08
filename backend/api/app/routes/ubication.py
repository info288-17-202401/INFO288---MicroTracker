from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.models.serialized_models import UbicationSerialized, Point #Como retorna la api
from app.models.models import Ubication #Obtiene desde la BD
import sys
# printstd = sys.stdout.write
# from geoalchemy2.elements import WKTElement
router = APIRouter()

@router.get("/", response_model=List[UbicationSerialized], status_code=200)
def get_ubications() -> Any:
    """
    Retrieve items.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        ubications = session.query(Ubication).all()
        # printstd("Ubications: ", ubications)
        # ubications_serialized = []
        # ubications
        # for ubication in ubications:
        #     ubication_serialized = UbicationSerialized(
        #         id=ubication.id,
        #         micro_patent=ubication.micro_patent,
        #         date=str(ubication.date),
        #         coordinates=Point(x=ubication.coordinates.x, y=ubication.coordinates.y),
        #         currently=ubication.currently
        #     )
        #     ubications_serialized.append(ubication_serialized)

        return ubications
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        session.close()
    

# @router.get("/{id}", response_model=UbicationSerialized, status_code=200)

@router.get("/{id}", response_model=UbicationSerialized, status_code=200)
def get_ubication(id: int) -> Any:
    """
    Get item by ID.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        ubication = session.query(Ubication).filter(Ubication.id == id).first()
        # print(ubication)
        if not ubication:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return ubication
    finally:
        session.close()


@router.post("/", response_model=Any, status_code=201)
def create_ubication(ubication: UbicationSerialized) -> Any:
    """
    Get item by ID.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        ubication = session.add(Ubication(
            micro_patent=ubication.micro_patent,
            date=ubication.date,
            coordinates=f"POINT({ubication.coordinates.x} {ubication.coordinates.y})",
            currently=ubication.currently
        ))
        session.commit()
        return {"ok": True, "status":201, "detail": "Ubication added"} 
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()