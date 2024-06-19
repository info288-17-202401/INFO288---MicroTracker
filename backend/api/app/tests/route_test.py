import pytest
import requests
# from . import app  # Asegúrate de importar tu aplicación FastAPI
from fastapi.testclient import TestClient
import sys
import os
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
URL_API = f"http://{HOST}:{PORT}"
current_directory = os.getcwd()

def test_get_routes():
    response = requests.get(f"{URL_API}/route/")
    assert response.status_code == 200
    routes = response.json()
    assert isinstance(routes, list)
    for route in routes:
        assert "id" in route
        assert "route" in route
        assert "line_id" in route
        assert isinstance(route["route"], list)
        for point in route["route"]:
            assert isinstance(point, dict)
            assert "x" in point
            assert "y" in point

@pytest.mark.parametrize("id", [1, 4])
def test_get_route(id: int):
    response = requests.get(f"{URL_API}/route/{id}")
    assert response.status_code == 200
    route = response.json()
    assert "id" in route
    assert "route" in route
    assert "line_id" in route
    assert isinstance(route["route"], list)
    for point in route["route"]:
        assert isinstance(point, dict)
        assert "x" in point
        assert "y" in point