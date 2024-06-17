from typing import List
from pydantic import BaseModel

# from geoalchemy2 import Geometry


##------------------
class Point(BaseModel):
    x: float
    y: float


##--------------------
class LineSerialized(BaseModel):
    number: int
    color: str

    class Config:
        from_attributes = True


class BrandSerialized(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ModelSerialized(BaseModel):
    id: int
    year: int
    name: str
    brand_id: int

    class Config:
        from_attributes = True


class SectorSerialized(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class MicrobusSerialized(BaseModel):
    patent: str
    line_id: int
    brand_id: int

    class Config:
        from_attributes = True


class BusStopSerialized(BaseModel):
    id: int
    coordinates: Point

    class Config:
        from_attributes = True


class PredictionResponse(BaseModel):
    microbus_id: str
    line_id: int
    time: float
    distance: float

    class Config:
        from_attributes = True


class PredictionCreate(BaseModel):
    lines_selected: List[int]
    busstop_id: int

    class Config:
        from_attributes = True


class RouteBusStopSerialized(BaseModel):
    route_id: int
    bus_stop_id: int

    class Config:
        from_attributes = True
