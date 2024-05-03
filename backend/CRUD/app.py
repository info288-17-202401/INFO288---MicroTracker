from fastapi import FastAPI
from main_routes import api_router


app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello World',
            'description': "LA TIPICA"}

app.include_router(api_router)

