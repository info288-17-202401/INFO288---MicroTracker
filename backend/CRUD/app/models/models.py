from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Microbus(Base):
    __tablename__ = 'microbus_sensor'
    patent = Column(String, primary_key=True, nullable=False)
    line = Column(Integer, nullable=False)
    def __repr__(self):
        return f"<Microbus(patent={self.patent}, line={self.line}>"

class MicrobusState(Base):
    __tablename__ = 'microbus_state'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    patent = Column(String, ForeignKey('microbus_sensor.patent'), nullable=False)
    # line = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    velocity = Column(Float, nullable=False)
    passengers = Column(Integer, nullable=False)  
    coordinates = Column(Geometry('POINT', srid=4326), nullable=False)
    currently = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<MicrobusState(id={self.id}, patent={self.patent}, date={self.date}, velocity={self.velocity}, passengers={self.passengers}, coordinates={self.coordinates}, currently={self.currently})>"
