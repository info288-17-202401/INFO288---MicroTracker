from .serialized_models import (
    MicrobusSerialized, 
    Point)
from typing import Optional

class MicrobusResponse(MicrobusSerialized):
    current_velocity: Optional[float]
    current_passengers: Optional[int]
    current_ubication: Optional[Point]
