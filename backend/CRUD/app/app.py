from fastapi import FastAPI
from fastapi import APIRouter
# from main_routes import api_router


app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello World',
            'description': "LA TIPICA"}

api_router = APIRouter()



# api_router.include_router(typedocument.router, prefix="/typedocument", tags=["typedocument"])
# api_router.include_router(author.router, prefix="/authors", tags=["authors"])
# api_router.include_router(document.router, prefix="/documents", tags=["documents"])

app.include_router(api_router)
