from fastapi import FastAPI
from app.routes.app_routes import api_router
from app.core.conexion_db import SessionLocal1, SessionLocal2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello World, Im the CRUD',
            'description': 'CRUD API working'}

@app.get('/db')
def index():
    sessions = [SessionLocal1(), SessionLocal2()]
    for session in sessions:
        try:
            session.execute(text("SELECT 1"))
        except Exception as e:
            return {
                'message': 'Cant connect to db',
                'description': str(e)
            }
        finally:
            session.close()
    return {'message': 'Hello World, Im the CRUD',
            'description': f'All database connections are working'}

@app.get('/hello')
def index():
    return {'message': 'Hello World, Im the CRUD',
            'description': "LA TIPICA"}

app.include_router(api_router)
