from .serialized_models import (
    MicrobusSerialized, 
    Point,
    UbicationSerialized,
    PassengersSerialized,
    VelocitySerialized
    )
from typing import Optional

class MicrobusResponse(MicrobusSerialized):
    # velocity: Optional[float]
    # passengers: Optional[int]
    coordinates: Optional[Point]

class UbicationResponse(UbicationSerialized):
    id: int
    # currently: bool

class PassengersResponse(PassengersSerialized):
    id: int
    # currently: bool

class VelocityResponse(VelocitySerialized):
    id: int
    # currently: bool
