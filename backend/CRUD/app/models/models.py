from sqlalchemy import (Column, Integer, String, ForeignKey, Date, Boolean, Float)
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Ubication(Base):
    __tablename__ = 'ubication'
    id = Column(Integer, primary_key=True, nullable=False)
    micro_patent = Column(String, ForeignKey('microbus.patent'), nullable=False)
    date =  Column(Date, nullable=False)
    coordinates = Column(Geometry("POINT"), nullable=False)
    actual = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Ubication(id={self.id}, micro_patent={self.micro_patent}, date={self.date}, coordinates={self.coordinates}, actual={self.actual})>"
    
class Microbus(Base):
    __tablename__ = 'microbus'
    patent = Column(String, primary_key=True, nullable=False)
    linea_id = Column(Integer, ForeignKey('line.number'), nullable=False)
    marca_id = Column(Integer, ForeignKey('brand.id'), nullable=False)
    def __repr__(self):
        return f"<Microbus(patent={self.patent}, linea_id={self.linea_id}, marca_id={self.marca_id})>"

class Line (Base):
    __tablename__ = 'line'
    number = Column(Integer, primary_key=True, nullable=False)
    color = Column(String, nullable=False)

    def __repr__(self):
        return f"<Line(number={self.number}, color={self.color})>"

class Passengers(Base):
    __tablename__ = 'passengers'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    micro_patent = Column(String, ForeignKey('microbus.patent'), nullable=False)
    number = Column(Integer, nullable=False)
    date =  Column(Date, nullable=False)
    actual = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Passengers(id={self.id}, micro_patent={self.micro_patent}, number={self.number}, date={self.date}, actual={self.actual})>"

class Route(Base):
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(Integer, nullable=False)
    date =  Column(Date, nullable=False)
    actual = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Route(id={self.id}, number={self.number}, date={self.date}, actual={self.actual})>"

class BusStop(Base):
    __tablename__ = 'bus_stop'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    coordinates = Column(Geometry("POINT"), nullable=False)
    id_ruta_fk = Column(Integer, ForeignKey('route.id'), nullable=False)

    def __repr__(self):
        return f"<BusStop(id={self.id}, coordinates={self.coordinates}, id_ruta_fk={self.id_ruta_fk})>"

class PredictionLogVelocity(Base):
    __tablename__ = 'prediction_log_velocity'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    velocidad = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    id_micro_fk = Column(String, ForeignKey('microbus.patent'), nullable=False)
    actual = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<PredictionLogVelocity(id={self.id}, velocidad={self.velocidad}, date={self.date}, id_micro_fk={self.id_micro_fk}, actual={self.actual})>"

class Sector(Base):
    __tablename__ = 'sector'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String, nullable=False)

    def __repr__(self):
        return f"<Sector(id={self.id}, nombre={self.nombre})>"
    
class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String, nullable=False)

    def __repr__(self):
        return f"<Brand(id={self.id}, nombre={self.nombre})>" 

class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    año = Column(Integer, nullable=False)
    nombre = Column(String, nullable=False)
    id_marca_fk = Column(Integer, ForeignKey('brand.id'), nullable=False)

    def __repr__(self):
        return f"<Model(id={self.id}, año={self.año}, nombre={self.nombre}, id_marca_fk={self.id_marca_fk})>"
