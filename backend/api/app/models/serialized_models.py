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
    name: str
    coordinates: Point

    class Config:
        from_attributes = True
