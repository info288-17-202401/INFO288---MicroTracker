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
from app.models.serialized_response_models import MicrobusResponse
import requests

# Obtener el objeto logger para tu aplicación
import logging

# Configura el nivel de registro
logging.basicConfig(level=settings.LOG_LEVEL)

# Crea un logger
logger = logging.getLogger(__name__)
URL_CRUD_MICROBUS = f"http://{settings.HOST_CRUD}:{settings.PORT_CRUD}/microbus/"
#TO DO: Que retorne la ubicacion actual tambien
router = APIRouter()


@router.get("/", response_model=List[MicrobusResponse], status_code=200)
def get_microbuses(id_lines: str | None = Query(None)) -> Any:
    """
    Retrieve all microbuses from line, if there's no id line, get all the microbuses.
    """
    try:
        session = SessionLocal()
        microbuses_from_db = []
        # Obtener microbuses de la base de datos
        if id_lines:
            for id_line in id_lines.split(" "):
                microbuses_from_db.extend(session.query(Microbus).filter(Microbus.line_id == int(id_line)).all())
        else:
            microbuses_from_db = session.query(Microbus).all()
        # Obtener patentes de los microbuses de la base de datos
        patents_from_db = [microbus.patent for microbus in microbuses_from_db]
        # Obtener microbuses de la solicitud filtrando por patentes
        response = requests.get(URL_CRUD_MICROBUS)
        logger.debug("RESPONSE:", response.json())
        if response.status_code == 200:
            microbuses_from_request = [microbus for microbus in response.json() if microbus.get('patent') in patents_from_db]
        else:
            microbuses_from_request = []
        # Combinar datos de la base de datos y de la solicitud
        microbuses_combined = []
        for microbus_data,microbus_db  in zip(microbuses_from_request,microbuses_from_db):
            logger.debug(f"Microbus data: {microbus_data}\n\nMicrobus db: {microbus_db}")
            combined_microbus = MicrobusResponse(
                patent=microbus_data.get("patent"),
                velocity=microbus_data.get("velocity"),
                passengers=microbus_data.get("passengers"),
                date= microbus_data.get("date"),
                #ITERA SOBRE LOS MICROBUSES DE LA BD Y BUSCA EL QUE TENGA LA PATENTE DE LA SOLICITUD
                line_id=next(filter(lambda microbus: getattr(microbus, "patent") ==  microbus_data.get("patent"),microbuses_from_db), None).line_id,
                coordinates=microbus_data.get("coordinates") if microbus_data else None,
                brand_id=next(filter(lambda microbus: getattr(microbus, "patent") ==  microbus_data.get("patent"),microbuses_from_db), None).brand_id
            )
            microbuses_combined.append(combined_microbus)

        logger.debug(f"Combined microbuses: {microbuses_combined}")

        if not microbuses_combined:
            raise HTTPException(status_code=404, detail="Microbuses not found")
        return microbuses_combined
    except Exception as e:
        logger.error(f"Can't connect to databases: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Can't connect to databases: {str(e)}")
    finally:
        session.close()
    
#TO DO: Retornar datos de micro seleccionada
@router.get("/{id}", response_model=MicrobusSerialized, status_code=200)
def get_microbus(id: str) -> Any:
    """
    Get item by ID.
    """
    try:
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
        session = SessionLocal()
        if response.status_code == 201:
            logger.debug('Solicitud exitosa CRUD')
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