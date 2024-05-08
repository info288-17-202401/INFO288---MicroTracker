from pydantic import BaseModel
# from geoalchemy2 import Geometry

##------------------
class Point(BaseModel):
    x: float
    y: float
##--------------------

class UbicationSerialized(BaseModel):
    id: int
    micro_patent: str
    date: str
    coordinates: Point
    currently: bool

    class Config:
        from_attributes = True
        
class MicrobusSerialized(BaseModel):
    patent: str
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


class VelocitySerialized(BaseModel):
    id: int
    velocity: float
    date: str
    micro_patent: str
    currently: bool

    class Config:
        from_attributes = True




