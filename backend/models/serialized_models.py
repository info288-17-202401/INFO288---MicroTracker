from pydantic import BaseModel


class UbicationSerialized(BaseModel):
    id: int
    micro_patent: str
    date: str
    coordinates: str
    actual: bool

    class Config:
        from_attributes = True


class MicrobusSerialized(BaseModel):
    patent: str
    linea_id: str
    marca_id: str

    class Config:
        from_attributes = True


class LineSerialized(BaseModel):
    number: int
    color: str

    class Config:
        from_attributes = True


class PassengersSerialized(BaseModel):
    id: int
    micro_patent: str
    number: int
    date: str
    actual: bool

    class Config:
        from_attributes = True


class RouteSerialized(BaseModel):
    id: int
    number: int
    date: str
    actual: bool

    class Config:
        from_attributes = True


class BusStopSerialized(BaseModel):
    id: int
    coordinates: str
    id_ruta_fk: int

    class Config:
        from_attributes = True


class PredictionLogVelocitySerialized(BaseModel):
    id: int
    velocidad: float
    date: str
    id_micro_fk: int
    actual: bool

    class Config:
        from_attributes = True


class SectorSerialized(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class BrandSerialized(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class ModelSerialized(BaseModel):
    id: int
    año: int
    nombre: str
    id_marca_fk: int

    class Config:
        from_attributes = True
