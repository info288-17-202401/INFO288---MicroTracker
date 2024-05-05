from pydantic import BaseModel
from geoalchemy2 import Geometry

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

class RouteSerialized(BaseModel):
    id: int
    number: int
    date: str
    currently: bool

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


class UbicationSerialized(BaseModel):
    id: int
    micro_patent: str
    date: str
    coordinates: Point
    currently: bool

    class Config:
        from_attributes = True



class PassengersSerialized(BaseModel):
    id: int
    micro_patent: str
    number: int
    date: str
    currently: bool

    class Config:
        from_attributes = True


class BusStopSerialized(BaseModel):
    id: int
    coordinates: str
    route_id: int

    class Config:
        from_attributes = True


class PredictionLogVelocitySerialized(BaseModel):
    id: int
    velocity: float
    date: str
    micro_patent: int
    currently: bool

    class Config:
        from_attributes = True




