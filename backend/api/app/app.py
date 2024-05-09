from fastapi import FastAPI
from app.routes.app_routes import api_router
from app.core.conexion_db import SessionLocal
from sqlalchemy import text

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello World, Im the Api',
            'description': 'ALL OK!'}

@app.get('/db')
def index():
    try:
        session = SessionLocal()
        got = session.execute(text("SELECT 1"))
    except Exception as e:
        return {
            'message': 'Cant connect to db',
            'description': str(e)
        }
    finally:
        session.close()
    return {'message': 'Hello World, Im the Api',
            'description': f'DB connected!'}

@app.get('/hello')
def index():
    return {'message': 'Hello World, Im the Api',
            'description': "LA TIPICA"}

app.include_router(api_router)
