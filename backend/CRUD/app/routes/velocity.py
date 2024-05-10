from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import SessionLocal
from fastapi import (APIRouter, 
                     HTTPException, 
                     Query)

from app.models.serialized_models import VelocitySerialized #Como retorna la api
from app.models.models import Velocity #Obtiene desde la BD

router = APIRouter()
@router.get("/", response_model=List[VelocitySerialized], status_code=200)
def get_velocities(currently: bool | None = Query(None)) -> Any:
    """
    Get velocities from all microbuses, if you want the current velocity, use query.
    """
    try:
        session = SessionLocal()
        if currently:
            velocity = session.query(Velocity).filter(Velocity.currently == currently).all()
        else:
            velocity = session.query(Velocity).all()
        # return velocity
    except Exception as e:
        raise HTTPException(status_code=404, msg="Can't connect to databases", detail=e)
    finally:
        session.close()
    return velocity
    

@router.get("/{patent}", response_model=VelocitySerialized, status_code=200)
def get_velocity(patent: str) -> Any:
    """
    Get current velocity from microbus .
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        velocity = session.get(Velocity).filter(Velocity.patent == patent and Velocity.currently == True).all()
        if not velocity:
            raise HTTPException(status_code=404, detail="Item not found")
        return velocity
    finally:
        session.close()

@router.post("/", response_model=Any, status_code=201)
def create_velocity(velocity: VelocitySerialized) -> Any:
    """
    Create velocity this needs a patent that exits.
    """
    try:
        session = SessionLocal()
        velocity = session.add(Velocity(
            velocity=velocity.velocity,
            date=velocity.date,
            patent=velocity.patent,
            currently=velocity.currently
        ))
        session.commit()
        return {"ok": True, "status":201, "detail": "Velocity added", "velocity": velocity} 
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()
    