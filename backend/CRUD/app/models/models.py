from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Microbus(Base):
    __tablename__ = 'microbus'
    patent = Column(String, primary_key=True, nullable=False)

    def __repr__(self):
        return f"<Microbus(patent={self.patent}>"

class Ubication(Base):
    __tablename__ = 'ubication'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    micro_patent = Column(String, ForeignKey('microbus.patent'), nullable=False)
    date = Column(Date, nullable=False)
    coordinates = Column(Geometry(geometry_type="POINT"), nullable=False)
    currently = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Ubication(id={self.id}, micro_patent={self.micro_patent}, date={self.date}, coordinates={self.coordinates}, currently={self.currently})>"

class Passengers(Base):
    __tablename__ = 'passengers'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    micro_patent = Column(String, ForeignKey('microbus.patent'), nullable=False)
    number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    currently = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Passengers(id={self.id}, micro_patent={self.micro_patent}, number={self.number}, date={self.date}, currently={self.currently})>"

class Velocity(Base):
    __tablename__ = 'velocity'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    velocity = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    micro_patent = Column(String, ForeignKey('microbus.patent'), nullable=False)
    currently = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Velocity(id={self.id}, velocity={self.velocity}, date={self.date}, micro_patent={self.micro_patent}, currently={self.currently})>"
