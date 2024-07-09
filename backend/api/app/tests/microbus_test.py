import pytest
import requests
import os
from dotenv import load_dotenv
from pydantic import ValidationError
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
URL_API = f"http://{HOST}:{PORT}"
current_directory = os.getcwd()
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))
from models.serialized_response_models import MicrobusResponse

# Función de prueba para la ruta get_microbuses
def test_get_microbuses():
    response = requests.get(f"{URL_API}/microbus")
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, list)  # Verifica que sea una lista
    # pytest.("Response is a list")
    for item in response_data:
        try:
            # Intenta crear una instancia del modelo MicrobusResponse
            microbus = MicrobusResponse(**item)
            print(microbus)
        except ValidationError as e:
            pytest.fail(f"Response item is not a valid MicrobusResponse: {e}")

        # Verifica que cada elemento sea una instancia de MicrobusResponse
        assert isinstance(microbus, MicrobusResponse)

