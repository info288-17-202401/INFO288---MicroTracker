from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import SessionLocal
from fastapi import (APIRouter, 
                     HTTPException, 
                     Query)
from sqlalchemy import text
from app.models.serialized_models import PassengersSerialized, Point #Como retorna la api
from app.models.models import Passengers #Obtiene desde la BD
# import sys
router = APIRouter()

@router.get("/", response_model=List[PassengersSerialized], status_code=200)
def get_passengers(patent: str | None = Query(None)) -> Any:
    """
    Retrieve items.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        if patent:
            passengers = session.query(Passengers).filter(Passengers.micro_patent == patent).all()
        else:
            passengers = session.query(Passengers).all()
        return passengers
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        session.close()

@router.get("/{patent}", response_model=PassengersSerialized, status_code=200)
def get_passengers(patent: str) -> Any:
    """
    Get last passenger of microbus by patent.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        passenger = session.query(Passengers).filter(Passengers.micro_patent == patent and Passengers.currently == True).first()
        # print(passenger)
        if not passenger:
            raise HTTPException(status_code=404, detail="Item not found")
        return passenger
    finally:
        session.close()

@router.post("/", response_model=Any, status_code=201)
def create_passenger(passenger: PassengersSerialized) -> Any:
    """
    Create passenger.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        passenger = session.add(Passengers(
            micro_patent=passenger.micro_patent,
            number=passenger.number,
            date=passenger.date,
            currently=passenger.currently
        ))
        session.commit()
        return {"ok": True, "status":201, "detail": "Passengers added"} 
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()