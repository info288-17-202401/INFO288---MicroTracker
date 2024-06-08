from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import SessionLocal, settings
import requests

# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException
from app.models.serialized_models import PredictionResponse, PredictionCreate
from app.models.models import BusStop, Microbus
from geoalchemy2.functions import ST_X, ST_Y


router = APIRouter()
URL_CRUD_MICROBUS = f"http://{settings.HOST_CRUD}:{settings.PORT_CRUD}/microbus/"


@router.get("/", response_model=List[PredictionResponse], status_code=200)
def get_predictions(prediction: PredictionCreate) -> Any:
    print(prediction)
    try:
        session = SessionLocal()
        selected_busstop = (
            session.query(BusStop).filter(BusStop.id == prediction.busstop_id).first()
        )
        x = session.query(ST_X(selected_busstop.coordinates)).scalar()
        y = session.query(ST_Y(selected_busstop.coordinates)).scalar()
        print(x, y)
        microbuses = (
            session.query(Microbus)
            .filter(Microbus.line_id.in_(prediction.lines_selected))
            .all()
        )
        print(microbuses)
        new = PredictionResponse(
            microbus_id="GGYL12",
            line_id=1,
            time=12.0,
            distance=1.0,
        )
        return [new]
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Can't connect to databases \n {str(e)}"
        )
    finally:
        session.close()
