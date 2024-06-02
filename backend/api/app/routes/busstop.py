from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import SessionLocal

# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException
from app.models.serialized_models import BusStopSerialized
from app.models.models import BusStop

router = APIRouter()


@router.get("/", response_model=List[BusStopSerialized], status_code=200)
def get_bus_stops() -> Any:
    try:
        session = SessionLocal()
        bus_stops = session.query(BusStop).all()

    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Can't connect to databases \n {str(e)}"
        )
    finally:
        session.close()
    return bus_stops
