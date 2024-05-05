from fastapi import FastAPI
# from fastapi import APIRouter
# from routes import microbus
from app.routes.app_routes import api_router
# from app.core.Settings import settings
from app.core.conexion_db import engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello World, Im the CRUD',
            'description': 'ALL OK!'}

@app.get('/DB')
def index():
    try:
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        got = session.execute(text("SELECT 1"))
    except Exception as e:
        return {
            'message': 'Cant connect to db',
            'description': str(e)
        }
    finally:
        session.close()
    return {'message': 'Hello World, Im the CRUD',
            'description': f'DB connected! query:{got}'}

@app.get('/hello')
def index():
    return {'message': 'Hello World, Im the CRUD',
            'description': "LA TIPICA"}

# api_router = APIRouter()

app.include_router(api_router)
