from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import engine
from sqlalchemy.orm import sessionmaker
from fastapi import (APIRouter, 
                     HTTPException, 
                     Query)
from geoalchemy2.shape import to_shape #geoalchemy2[shapely]
from app.models.serialized_models import (MicrobusSerialized, 
                                          Point)
from app.models.serialized_response_models import (
    MicrobusResponse
    )
from app.models.models import (Microbus, 
                               Ubication, 
                               Passengers,
                               Velocity)
# from app.core.Settings import settings

# Obtener el objeto logger para tu aplicación
router = APIRouter()
@router.get("/", response_model=List[MicrobusSerialized], status_code=200)
def get_microbuses() -> Any:
    """
    Retrieve all microbuses from line, if there's no id line, get all the microbuses.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        microbus = session.query(Microbus).all()
        # return microbus
    except Exception as e:
        raise HTTPException(status_code=404, detail="Can't connect to databases")
    finally:
        session.close()
    return microbus
    

@router.get("/{patent}", response_model=MicrobusResponse, status_code=200)
def get_microbus(patent: str) -> Any:
    """
    Get all current data from the microbuses using patent.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        microbus = session.query(Microbus).filter(Microbus.patent == patent).first()
        if not microbus:
            raise HTTPException(status_code=404, detail="Item not found")
        
         # Obtener los pasajeros actuales
        passengers = session.query(Passengers).filter(Passengers.micro_patent == patent, Passengers.currently == True).first()
        # Obtener la velocidad actual
        velocity = session.query(Velocity).filter(Velocity.micro_patent == patent, Velocity.currently == True).first()
        # Obtener la ubicación actual
        ubication = session.query(Ubication).filter(Ubication.micro_patent == patent, Ubication.currently == True).first()
        if ubication:
            ubication = to_shape(ubication.coordinates)
        microbus_serialized = MicrobusResponse(
            patent = microbus.patent,
            current_velocity = velocity.velocity if velocity else None,
            current_passengers = passengers.number if passengers else None,
            current_ubication = Point(x = ubication.x, y = ubication.y) if ubication else None
        )
        return microbus_serialized
        
    finally:
        session.close()

@router.post("/", response_model=Any, status_code=201)
def create_microbus(microbus: MicrobusSerialized) -> Any:
    """
    Get item by ID.
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        microbus =session.add(Microbus(
            patent = microbus.patent
        ))
        session.commit()
        return {"ok": True, "status":201, "detail": "Microbus added", "microbus": microbus} 
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()