from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import SessionLocal

# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException
from app.models.serialized_models import BusStopSerialized, Point
from app.models.models import BusStop
from geoalchemy2.functions import ST_X, ST_Y

router = APIRouter()


@router.get("/", response_model=List[BusStopSerialized], status_code=200)
def get_bus_stops() -> Any:
    try:
        session = SessionLocal()
        bus_stops = session.query(BusStop).all()
        bus_stop_serialized = []
        for bus_stop in bus_stops:
            x = session.query(ST_X(bus_stop.coordinates)).scalar()
            y = session.query(ST_Y(bus_stop.coordinates)).scalar()
            bus_stop_serialized.append(
                BusStopSerialized(
                    id=bus_stop.id,
                    coordinates=Point(x=x, y=y),
                )
            )
        return bus_stop_serialized
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Can't connect to databases \n {str(e)}"
        )
    finally:
        session.close()


@router.get("/{id}", response_model=BusStopSerialized, status_code=200)
def get_bus_stop(id: int) -> Any:
    try:
        session = SessionLocal()
        bus_stop = session.get(BusStop, id)
        if not bus_stop:
            raise HTTPException(status_code=404, detail="Item not found")
        bus_stop_serialized = BusStopSerialized(
            id=bus_stop.id,
            coordinates=Point(
                x=session.query(ST_X(bus_stop.coordinates)).scalar(),
                y=session.query(ST_Y(bus_stop.coordinates)).scalar(),
            ),
        )
        return bus_stop_serialized
    finally:
        session.close()
