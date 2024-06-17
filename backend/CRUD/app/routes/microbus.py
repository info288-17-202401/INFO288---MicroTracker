from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import databases_settings, sessions, getCorrectSession

# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException, Query
from geoalchemy2.shape import to_shape  # geoalchemy2[shapely]
from app.models.serialized_models import (MicrobusSerialized, MicrobusResponse, Point)
# from app.models.serialized_response_models import MicrobusResponse
from app.models.models import Microbus, MicrobusState
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
    all_microbuses_response = []  # Mueve la declaración fuera del bucle
    for session in sessions:
        try:
            session = session()
            microbuses = session.query(Microbus).all()
            for microbus in microbuses:
                microbus_state = (
                    session.query(MicrobusState)
                    .filter(
                        MicrobusState.patent == microbus.patent,
                        MicrobusState.currently == True,
                    )
                    .first()
                )
                if microbus_state:
                    coordinates = to_shape(microbus_state.coordinates)
                    # Crea el objeto MicrobusResponse
                    microbus_response = MicrobusResponse(
                        line=microbus.line,
                        patent=microbus.patent,
                        velocity=microbus_state.velocity if microbus_state else None,
                        passengers=microbus_state.passengers if microbus_state else None,
                        coordinates=Point(x=coordinates.x, y=coordinates.y) if coordinates else None,
                        date=str(microbus_state.date) if microbus_state else None,
                    )
                    # Agrega el objeto MicrobusResponse a la lista de respuestas
                    all_microbuses_response.append(microbus_response)
            logger.debug(f"Response microbuses: {all_microbuses_response}")
        except Exception as e:
            # Loguea cualquier error
            logger.error(f"Error al procesar microbuses: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        finally:
            session.close()
    return all_microbuses_response  # Devuelve la lista acumulada fuera del bucle

@router.post("/", response_model=Any, status_code=201)
def create_microbus(microbus: MicrobusSerialized) -> Any:
    """
    Get item by ID.
    """
    try:
        session = getCorrectSession(microbus.line)
        session = session()
        microbus = session.add(Microbus(patent=microbus.patent, line=microbus.line))
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
