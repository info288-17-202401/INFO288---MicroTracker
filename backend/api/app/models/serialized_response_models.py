from .serialized_models import (
    MicrobusSerialized, 
    Point)
from typing import Optional

class MicrobusResponse(MicrobusSerialized):
    coordinates: Optional[Point]
