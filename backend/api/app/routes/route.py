from typing import (
    Any,
    # Optional,
    List,
)
from app.core.conexion_db import SessionLocal

# from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, HTTPException
from app.models.serialized_models import RouteSerialized, Point
from app.models.models import Route
# from geoalchemy2.functions import ST_X, ST_Y
# from geoalchemy2.elements import WKTElement
# from shapely.geometry import MultiPoint
# from shapely import wkt
from sqlalchemy import func

router = APIRouter()

@router.get("/", response_model=List[RouteSerialized], status_code=200)
def get_routes() -> Any:
    try:
        session = SessionLocal()
        routes = session.query(Route).all()
        print(routes)
        routes_serialized = []
        for route in routes:
            coordinates = []
            multipoint_wkt = session.query(func.ST_AsText(route.route)).scalar()
            multipoint_wkt = multipoint_wkt.replace("MULTIPOINT((", "").replace("))", "")
            points = multipoint_wkt.split("),(")
            for point in points:
                x, y = point.split()
                coordinates.append(Point(x=float(x), y=float(y)))

            route_serialized = RouteSerialized(
                id=route.id,
                route=coordinates,
                line_id=route.line_id
            )
            routes_serialized.append(route_serialized)
        return routes_serialized

    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Can't connect to databases \n {str(e)}"
        )
    finally:
        session.close()


@router.get("/{line_id}", response_model=RouteSerialized, status_code=200)
def get_route(line_id: int) -> Any:
    try:
        session = SessionLocal()
        route = session.query(Route).filter(Route.line_id == line_id).first()
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")

        coordinates = []
        multipoint_wkt = session.query(func.ST_AsText(route.route)).scalar()
        multipoint_wkt = multipoint_wkt.replace("MULTIPOINT((", "").replace("))", "")
        points = multipoint_wkt.split("),(")
        for point in points:
            x, y = point.split()
            coordinates.append(Point(x=float(x), y=float(y)))

        route_serialized = RouteSerialized(
            id=route.id,
            route=coordinates,
            line_id=route.line_id
        )
        return route_serialized
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Error retrieving route: {str(e)}"
        )
    finally:
        session.close()

