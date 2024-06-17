from pydantic import BaseModel
from typing import Optional
# from geoalchemy2 import Geometry

##------------------
class Point(BaseModel):
    x: float
    y: float
##--------------------

"""
SE AGREGO CLASE RESPONSE PARA TODAS
"""
class MicrobusStateSerialized(BaseModel):
    # id: int
    patent: str
    line: int
    date: str
    velocity: float
    passengers: int
    coordinates: Point
    currently: bool

    class Config:
        from_attributes = True

class MicrobusStateResponse(MicrobusStateSerialized):
    id: int
    # currently: bool

class MicrobusSerialized(BaseModel):
    patent: str
    line: int
    class Config:
        from_attributes = True


class MicrobusResponse(MicrobusSerialized):
    velocity: Optional[float]
    passengers: Optional[int]
    coordinates: Optional[Point]
    date: Optional[str]




