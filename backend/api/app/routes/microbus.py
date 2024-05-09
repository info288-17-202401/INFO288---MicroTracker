from typing import (Any, 
                    # Optional, 
                    List)
from app.core.conexion_db import SessionLocal, settings
# from sqlalchemy import create_engine
from fastapi import (APIRouter, 
                     HTTPException, 
                     Query)

from app.models.serialized_models import MicrobusSerialized
from app.models.models import Microbus
import requests
# from app.core.Settings import settings

# Obtener el objeto logger para tu aplicación
import logging

# Configura el nivel de registro
logging.basicConfig(level=settings.LOG_LEVEL)

# Crea un logger
logger = logging.getLogger(__name__)
URL_CRUD_MICROBUS = f"http://{settings.HOST_CRUD}:{settings.PORT_CRUD}/microbus/"
#TO DO: Que retorne la ubicacion actual tambien
router = APIRouter()
@router.get("/", response_model=List[MicrobusSerialized], status_code=200)
def get_microbuses(id_lines: str | None = Query(None)) -> Any:
    """
    Retrieve all microbuses from line, if there's no id line, get all the microbuses.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        microbuses = []
        if id_lines:
            for id_line in id_lines.split(" "):
                microbus = session.query(Microbus).filter(Microbus.line_id == int(id_line)).all()
                if microbus:
                    microbuses.extend(microbus)
        else:
            microbus = session.query(Microbus).all()
        if not microbuses:
            logger.debug("Microbuses not found")
            raise HTTPException(status_code=404, detail="Microbuses not found")
        # return microbus
        microbuses_crud = requests.get(URL_CRUD_MICROBUS)
        logger.debug(f"Microbuses CRUD: {microbuses_crud.json()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Can't connect to databases")
    finally:
        session.close()
    return microbus
    
#TO DO: Retornar datos de micro seleccionada
@router.get("/{id}", response_model=MicrobusSerialized, status_code=200)
def get_microbus(id: str) -> Any:
    """
    Get item by ID.
    """
    try:
        # SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        microbus = session.get(Microbus, id)
        if not microbus:
            raise HTTPException(status_code=404, detail="Item not found")
        return microbus
        
    finally:
        session.close()

@router.post("/", response_model=Any, status_code=201)
def create_microbus(microbus: MicrobusSerialized) -> Any:
    """
    Get item by ID.
    """
    try:
        response = requests.post(URL_CRUD_MICROBUS, json={"patent":microbus.patent})
        if response.status_code == 201:
            logger.debug('Solicitud exitosa CRUD')
            session = SessionLocal()
            microbus_added = session.add(Microbus(
                patent = microbus.patent,
                line_id = microbus.line_id,
                brand_id = microbus.brand_id
            ))
            session.commit() 
        else:
            logger.debug('Error en la solicitud:', response.status_code)
            raise HTTPException(status_code=500, detail="Can't connect to db")
        return {"ok": True, "status":201, "detail": "Microbus added", "microbus": microbus} 
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cant add item \n {str(e)}")
    finally:
        session.close()