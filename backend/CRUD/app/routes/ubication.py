from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import SessionLocal
from fastapi import APIRouter, HTTPException, Query

# Como retorna la api
from app.models.serialized_models import UbicationSerialized, Point
from app.models.models import Ubication  # Obtiene desde la BD
import logging

router = APIRouter()

# Configura el nivel de registro
logging.basicConfig(level=logging.DEBUG)

# Crea un logger
logger = logging.getLogger(__name__)

# Importar el módulo Point de pydantic
"""
NO SE USARA
"""


@router.get("/", response_model=List[UbicationSerialized], status_code=200)
def get_ubications(patent: str | None = Query(None)) -> Any:
    """
    Retrieve items.
    """
    try:
        session = SessionLocal()
        if patent:
            ubications = session.query(Ubication).filter(Ubication.patent == patent).all()
        else:
            ubications = session.query(Ubication).all()
        logger.debug(f"Ubications: {ubications}")
        if not ubications:
            logger.debug(f"Ubications not found")
            raise HTTPException(status_code=404, detail="Items not found")

        # Serializar los objetos Ubication a UbicationSerialized
        ubications_serialized = []
        for ubication in ubications:
            ubication_serialized = UbicationSerialized(
                id=ubication.id,
                patent=ubication.patent,
                date=str(ubication.date),
                coordinates=Point(x=ubication.coordinates.x, y=ubication.coordinates.y),
                currently=ubication.currently,
            )
            ubications_serialized.append(ubication_serialized)

        return ubications_serialized
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error:\n {str(e)}")
    finally:
        session.close()


##No se usara
@router.get("/{patent}", response_model=UbicationSerialized, status_code=200)
def get_ubication(patent: str) -> Any:
    """
    Get last ubication of microbus by patent.
    """
    try:
        session = SessionLocal()
        ubication = (
            session.query(Ubication)
            .filter(Ubication.micro_patent == patent and Ubication.currently == True)
            .first()
        )
        if not ubication:
            raise HTTPException(status_code=404, detail="Item not found")
        return ubication
    finally:
        session.close()


# TO DO:Cambiar
@router.post("/", response_model=Any, status_code=201)
def create_ubication(ubication: UbicationSerialized) -> Any:
    """
    Create ubication.
    """
    try:
        session = SessionLocal()
        ubication = session.add(
            Ubication(
                micro_patent=ubication.micro_patent,
                date=ubication.date,
                coordinates=f"POINT({ubication.coordinates.x} {ubication.coordinates.y})",
                currently=ubication.currently,
            )
        )
        session.commit()
        return {"ok": True, "status": 201, "detail": "Ubication added"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()
