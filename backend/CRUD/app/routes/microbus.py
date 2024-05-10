from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import SessionLocal

# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException, Query
from geoalchemy2.shape import to_shape  # geoalchemy2[shapely]
from app.models.serialized_models import MicrobusSerialized, Point
from app.models.serialized_response_models import MicrobusResponse
from app.models.models import Microbus, Ubication, Passengers, Velocity
import logging

# Configura el nivel de registro
logging.basicConfig(level=logging.DEBUG)

# Crea un logger
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[MicrobusResponse], status_code=200)
def get_microbuses() -> Any:
    """
    Retrieve all microbuses from line, if there's no id line, get all the microbuses.
    """
    try:
        session = SessionLocal()
        microbuses = session.query(Microbus).all()
        microbuses_response = []
        for microbus in microbuses:
            # Obtener los pasajeros actuales
            # passengers = session.query(Passengers).filter(Passengers.patent == microbus.patent, Passengers.currently == True).first()
            # Obtener la velocidad actual
            # velocity = session.query(Velocity).filter(Velocity.patent == microbus.patent, Velocity.currently == True).first()
            # Obtener la ubicación actual
            ubication = (
                session.query(Ubication)
                .filter(
                    Ubication.micro_patent == microbus.patent,
                    Ubication.currently == True,
                )
                .first()
            )
            if ubication:
                ubication = to_shape(ubication.coordinates)
            # Crea el objeto MicrobusResponse
            microbus_response = MicrobusResponse(
                patent=microbus.patent,
                # current_velocity=velocity.velocity if velocity else None,
                # current_passengers=passengers.number if passengers else None,
                coordinates=Point(x=ubication.x, y=ubication.y) if ubication else None,
            )
            # Agrega el objeto MicrobusResponse a la lista de respuestas
            microbuses_response.append(microbus_response)
        logger.debug(f"Response microbuses: {microbuses_response}")
        return microbuses_response

    except Exception as e:
        # Loguea cualquier error
        logger.error(f"Error al procesar microbuses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    finally:
        session.close()


@router.get("/{patent}", response_model=MicrobusResponse, status_code=200)
def get_microbus(patent: str):
    try:
        session = SessionLocal()

        # Obtener el microbús específico por su patente
        microbus = session.query(Microbus).filter(Microbus.patent == patent).first()

        if not microbus:
            raise HTTPException(status_code=404, detail="Microbus not found")

        # Obtener los pasajeros actuales
        passengers = (
            session.query(Passengers)
            .filter(Passengers.micro_patent == patent, Passengers.currently == True)
            .first()
        )
        # Obtener la velocidad actual
        velocity = (
            session.query(Velocity)
            .filter(Velocity.micro_patent == patent, Velocity.currently == True)
            .first()
        )
        # Obtener la ubicación actual
        # ubication = session.query(Ubication).filter(Ubication.patent == patent, Ubication.currently == True).first()
        # if ubication:
        #     ubication = to_shape(ubication.coordinates)

        # Crear el objeto MicrobusResponse
        microbus_response = MicrobusResponse(
            patent=microbus.patent,
            velocity=velocity.velocity if velocity else None,
            passengers=passengers.number if passengers else None,
            # coordinates=Point(x=ubication.x, y=ubication.y) if ubication else None
        )

        logger.debug(f"Response microbus: {microbus_response}")

        return microbus_response

    except Exception as e:
        # Loguear cualquier error
        logger.error(f"Error al procesar microbus: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    finally:
        session.close()


@router.post("/", response_model=Any, status_code=201)
def create_microbus(microbus: MicrobusSerialized) -> Any:
    """
    Get item by ID.
    """
    try:
        session = SessionLocal()
        microbus = session.add(Microbus(patent=microbus.patent))
        session.commit()
        return {
            "ok": True,
            "status": 201,
            "detail": "Microbus added",
            "microbus": microbus,
        }
    except Exception as e:
        logger.error(f"{str(e)}")
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()
