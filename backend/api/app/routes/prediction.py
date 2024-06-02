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

router = APIRouter()
URL_CRUD_MICROBUS = f"http://{settings.HOST_CRUD}:{settings.PORT_CRUD}/microbus/"


@router.get("/", response_model=List[PredictionResponse], status_code=200)
def get_predictions(prediction: PredictionCreate) -> Any:
    try:
        session = SessionLocal()
        selected_busstop = (
            session.query(BusStop).filter(BusStop.id == prediction.busstop_id).first()
        )
        print(selected_busstop)
        microbuses = (
            session.query(Microbus)
            .filter(Microbus.line_id.in_(prediction.lines_selected))
            .all()
        )
        print(microbuses)
        new = PredictionResponse(
            microbus_id="XD",
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
