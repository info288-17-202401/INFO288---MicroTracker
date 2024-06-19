import pytest
import requests
# from fastapi.testclient import TestClient
# from app.main import app  # Asegúrate de importar tu aplicación FastAPI
# from app.core.conexion_db import SessionLocal
# from models.models import BusStop
# from sqlalchemy import func
# from typing import List, Any

import sys
import os
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()
from models.serialized_models import BusStopSerialized, Point
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
URL_API = f"http://{HOST}:{PORT}"
current_directory = os.getcwd()



def test_get_bus_stops():
    # Mock de la sesión de base de datos para evitar interacciones reales con la base de datos

    # Ejecutar la solicitud GET a la ruta de la API
    response = requests.get(f"{URL_API}/busstop/")
    
    # Verificar el código de estado de la respuesta
    assert response.status_code == 200
    
    # Verificar el tipo de datos devueltos
    bus_stops = response.json()
    assert isinstance(bus_stops, list)

    # Verificar que cada elemento en la lista sea un objeto BusStopSerialized válido
    for bus_stop in bus_stops:
        assert "id" in bus_stop
        assert "coordinates" in bus_stop
        assert isinstance(bus_stop["coordinates"], dict)
        point = Point(**bus_stop["coordinates"])
        assert isinstance(point, Point)

