from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import SessionLocal, settings
import requests

# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException
from app.models.serialized_models import (
    PredictionResponse,
    PredictionCreate,
    RouteBusStopSerialized,
)
from app.models.models import BusStop, Microbus, RouteBusStop, Route, Line
from geoalchemy2.functions import ST_X, ST_Y
from sqlalchemy import func

# Obtener el objeto logger para tu aplicación
import logging

# Configura el nivel de registro
logging.basicConfig(level=settings.LOG_LEVEL)

# Crea un logger
logger = logging.getLogger(__name__)

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
        route_busstop_all = (
            session.query(RouteBusStop)
            .filter(RouteBusStop.id_busstop_fk == prediction.busstop_id)
            .all()
        )
        ids = [route.id_ruta_fk for route in route_busstop_all]
        routes = session.query(Route).filter(Route.id.in_(ids)).all()
        lines = [route.line_id for route in routes]
        microbuses = (
            session.query(Microbus)
            .filter(Microbus.line_id.in_(prediction.lines_selected))
            .filter(Microbus.line_id.in_(lines))
            .all()
        )
        microbus_patents = {
            microbus.patent: microbus.line_id for microbus in microbuses
        }

        response = requests.get(URL_CRUD_MICROBUS)
        microbus_all = [
            {**microbus, "line": microbus_patents[microbus.get("patent")]}
            for microbus in response.json()
            if microbus.get("patent") in microbus_patents
        ]
        distances = []
        print(microbus_all)
        for micro in microbus_all:
            current_route = (
                session.query(Route).filter(Route.line_id == micro["line"]).first()
            )
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
