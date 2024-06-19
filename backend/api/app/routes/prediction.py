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
from geoalchemy2 import WKTElement, functions as geofunc

# Obtener el objeto logger para tu aplicación
import logging

# Configura el nivel de registro
logging.basicConfig(level=settings.LOG_LEVEL)

# Crea un logger
logger = logging.getLogger(__name__)


router = APIRouter()
URL_CRUD_MICROBUS = f"http://{settings.HOST_CRUD}:{settings.PORT_CRUD}/microbus/"
METTERS_PER_DEGREE = 111139


@router.get("/", response_model=List[PredictionResponse], status_code=200)
def get_predictions(prediction: PredictionCreate) -> Any:
    try:

        predictions = []
        session = SessionLocal()
        results = (
            session.query(Microbus.patent, Route.route, Line.number, Line.color)
            .join(Line, Microbus.line_id == Line.number)
            .join(Route, Line.number == Route.line_id)
            .join(RouteBusStop, Route.id == RouteBusStop.id_ruta_fk)
            .join(BusStop, RouteBusStop.id_busstop_fk == BusStop.id)
            .filter(BusStop.id == prediction.busstop_id)
            .filter(Line.number.in_(prediction.lines_selected))
            .all()
        )
        selected_busstop = (
            session.query(BusStop).filter(BusStop.id == prediction.busstop_id).first()
        )
        x = session.query(ST_X(selected_busstop.coordinates)).scalar()
        y = session.query(ST_Y(selected_busstop.coordinates)).scalar()
        selected_busstop_coordinates = (x, y)
        # route_busstop_all = (
        #     session.query(RouteBusStop)
        #     .filter(RouteBusStop.id_busstop_fk == prediction.busstop_id)
        #     .all()
        # )
        # ids = [route.id_ruta_fk for route in route_busstop_all]
        # routes = session.query(Route).filter(Route.id.in_(ids)).all()
        # lines = [route.line_id for route in routes]
        # microbuses = (
        #     session.query(Microbus)
        #     .filter(Microbus.line_id.in_(prediction.lines_selected))
        #     .filter(Microbus.line_id.in_(lines))
        #     .all()
        # )
        # microbus_patents = {
        #     microbus.patent: microbus.line_id for microbus in microbuses
        # }
        # print(microbus_patents)
        response = requests.get(URL_CRUD_MICROBUS)
        print(response.json())
        microbus_all = [
            micro
            for micro in response.json()
            if micro["line"] in prediction.lines_selected
            and micro["patent"] in [result.patent for result in results]
        ]
        distances = []
        print(microbus_all)
        for micro in microbus_all:
            total_distance = []
            current_route = next(
                (
                    result.route
                    for result in results
                    if result.patent == micro["patent"]
                ),
                None,
            )
            microbus_coordinates = (
                float(micro["coordinates"]["x"]),
                float(micro["coordinates"]["y"]),
            )
            coordinates = []
            multipoint_wkt = session.query(func.ST_AsText(current_route)).scalar()
            multipoint_wkt = multipoint_wkt.replace("MULTIPOINT((", "").replace(
                "))", ""
            )
            points = multipoint_wkt.split("),(")
            index = 0
            start = 0
            end = 0
            for point in points:
                x, y = point.split()
                new = (float(x), float(y))
                coordinates.append(new)
                if new == microbus_coordinates:
                    print("LOOOOOOOOOOL")
                    start = index
                if new == selected_busstop_coordinates:
                    print("XDDDDDDDD")
                    end = index
                index += 1
            if start != 0 and start < end:
                for i in range(start, end - 1):
                    point1 = func.ST_SetSRID(
                        geofunc.ST_MakePoint(coordinates[i][0], coordinates[i][1]), 4326
                    )
                    point2 = func.ST_SetSRID(
                        geofunc.ST_MakePoint(
                            coordinates[i + 1][0], coordinates[i + 1][1]
                        ),
                        4326,
                    )
                    distance = session.query(func.ST_Distance(point1, point2)).scalar()
                    total_distance.append(distance)
                distances.append(sum(total_distance) * METTERS_PER_DEGREE)
                print(distances)
                new = PredictionResponse(
                    microbus_id=micro["patent"],
                    line_id=micro["line"],
                    time=round(
                        (
                            ((sum(total_distance) * METTERS_PER_DEGREE) / 1000)
                            / micro["velocity"]
                        )
                        * 60,
                        2,
                    ),
                    distance=round(sum(total_distance) * METTERS_PER_DEGREE, 2),
                )
                predictions.append(new)
        # new = PredictionResponse(
        #     microbus_id="GGYL12",
        #     line_id=1,
        #     time=12.0,
        #     distance=1.0,
        # )

        # x1 = -39.540203
        # y1 = -72.968864
        # x2 = -39.540271
        # y2 = -72.968869
        # test_point_1 = func.ST_SetSRID(geofunc.ST_MakePoint(x1, y1), 4326)
        # test_point_2 = func.ST_SetSRID(geofunc.ST_MakePoint(x2, y2), 4326)
        # distance2 = session.query(func.ST_Distance(test_point_1, test_point_2)).scalar()
        # print("TEST", distance2 * METTERS_PER_DEGREE)
        return predictions
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Can't connect to databases \n {str(e)}"
        )
    finally:
        session.close()
