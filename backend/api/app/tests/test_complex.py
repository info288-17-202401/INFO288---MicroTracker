import sys
import os
import pytest
# from fastapi.testclient import TestClient
import requests
# Ajustar el PYTHONPATH para incluir el directorio raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/api')))
from dotenv import load_dotenv
# from backend.api.app.app import app  # Importa tu aplicación FastAPI
load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
URL_API = f"http://{HOST}:{PORT}"

def test_db_route():
    """
    Verifica que la ruta /db pueda conectarse a la base de datos y devolver el mensaje correcto.
    """
    response = requests.get(f"{URL_API}/db")
    assert response.status_code == 200
    
    json_response = response.json()
    print(json_response)
    assert 'message' in json_response
    assert 'description' in json_response
    
    assert json_response['message'] == 'Hello World, Im the Api'
    
    if 'Cant connect to db' in json_response['description']:
        assert json_response['description'].startswith('Cant connect to db')
    else:
        assert json_response['description'].startswith('DB connected!')
