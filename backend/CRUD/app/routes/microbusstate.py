from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import sessions, databases_settings, getCorrectSession
from fastapi import APIRouter, HTTPException, Query

# Como retorna la api
from app.models.serialized_models import (
    MicrobusStateSerialized,
    MicrobusStateResponse,
    Point,
)
from app.models.models import MicrobusState  # Obtiene desde la BD
import logging
from geoalchemy2.shape import to_shape


router = APIRouter()

# Configura el nivel de registro
logging.basicConfig(level=logging.DEBUG)

# Crea un logger
logger = logging.getLogger(__name__)

# Importar el módulo Point de pydantic
"""
NO SE USARA
"""
@router.get("/", response_model=List[MicrobusStateResponse], status_code=200)
def get_microbus_states(patent: str | None = Query(None)) -> Any:
    """
    Retrieve items.
    """
    for session in sessions:
        try:
            session = session()
            if patent:
                microbus_states = (
                    session.query(MicrobusState)
                    .filter(MicrobusState.patent == patent)
                    .all()
                )
            else:
                microbus_states = session.query(MicrobusState).all()
            logger.debug(f"MicrobusState: {microbus_states}")
            if not microbus_states:
                logger.debug(f"MicrobusState not found")
                raise HTTPException(status_code=404, detail="Items not found")
            # logger.debug(f"---------")
            # Serializar los objetos MicrobusState a MicrobusStateSerialized
            microbus_states_serialized = []
            for state in microbus_states:
                logger.debug(f"State: {state}")
                coordinates = to_shape(state.coordinates)
                state_serialized = MicrobusStateResponse(
                    id=state.id,
                    patent=state.patent,
                    date=str(state.date),
                    velocity=state.velocity,
                    passengers=state.passengers,
                    coordinates=Point(x=coordinates.x, y=coordinates.y),
                    currently=state.currently,
                )
                microbus_states_serialized.append(state_serialized)
            logger.debug(f"MicrobusState serialized: {microbus_states_serialized}")
            return microbus_states_serialized
        except Exception as e:
            logger.error(f"Error: {e}")
            raise HTTPException(status_code=500, detail=f"Internal error:\n {str(e)}")
        finally:
            session.close()



# TO DO:Cambiar
@router.post("/", response_model=Any, status_code=201)
def create_state(microbus_state: MicrobusStateSerialized) -> Any:
    """
    Create microbus_state.
    """
    try:
        session = getCorrectSession(microbus_state.line)
        session = session()
        microbus_state = session.add(
            MicrobusState(
                patent=microbus_state.patent,
                # line=microbus_state.line,
                date=microbus_state.date,
                velocity=microbus_state.velocity,
                passengers=microbus_state.passengers,
                coordinates=f"POINT({microbus_state.coordinates.x} {microbus_state.coordinates.y})",
                currently=microbus_state.currently,
            )
        )
        session.commit()
        return {"ok": True, "status": 201, "detail": "MicrobusState added"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()
