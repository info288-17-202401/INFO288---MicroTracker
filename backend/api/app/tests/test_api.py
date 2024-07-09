import sys
import os
import pytest
from fastapi.testclient import TestClient
import requests
# Ajustar el PYTHONPATH para incluir el directorio raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/api')))

# from backend.api.app.app import app  # Importa tu aplicación FastAPI
# from backend.api.app.models.models import Microbus  # Importa tu modelo de base de datos
from dotenv import load_dotenv
load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
URL_API = f"http://{HOST}:{PORT}"

def test_hello():
    response = requests.get(f"{URL_API}/hello")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Hello World, Im the Api',
        'description': 'LA TIPICA'
    }
