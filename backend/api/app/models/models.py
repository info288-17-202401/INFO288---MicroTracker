from sqlalchemy import (Column, 
                        Integer, 
                        String, 
                        ForeignKey, 
                        # Date, 
                        # Boolean, 
                        # Float
    )
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base

Base = declarative_base()
### Hacer tabla de relacion de sector y linea
### Hacer relacion de paradero con linea, no con ruta
### Cual es la diferencia entre linea y route...
### Pensar si dejar las ubicaciones (puntos) en una tabla (para no repetir ubicaciones)

class Line(Base):
    __tablename__ = 'line'
    number = Column(Integer, primary_key=True, nullable=False)
    color = Column(String, nullable=False)
    # route = Columm([])
    #arreglo de ruta
    def __repr__(self):
        return f"<Line(number={self.number}, color={self.color})>"

class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Brand(id={self.id}, name={self.name})>"

class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True, nullable=False)
    year = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)

    def __repr__(self):
        return f"<Model(id={self.id}, year={self.year}, name={self.name}, brand_id={self.brand_id})>"

    def __repr__(self):
        return f"<Route(id={self.id}, number={self.number}, date={self.date}, currently={self.currently})>"

class Sector(Base):
    __tablename__ = 'sector'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Sector(id={self.id}, name={self.name})>"

class Microbus(Base):
    __tablename__ = 'microbus'
    patent = Column(String, primary_key=True, nullable=False)
    line_id = Column(Integer, ForeignKey('line.number'), nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)

    def __repr__(self):
        return f"<Microbus(patent={self.patent}, line_id={self.line_id}, brand_id={self.brand_id})>"

##Pensar si ponerle una flag a la ubicacion para decir que es un paradero
class BusStop(Base):
    __tablename__ = 'bus_stop'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    coordinates = Column(Geometry(geometry_type="POINT"), nullable=False)
    route_id = Column(Integer, ForeignKey('route.id'), nullable=False)

    def __repr__(self):
        return f"<BusStop(id={self.id}, coordinates={self.coordinates}, route_id={self.route_id})>"
    