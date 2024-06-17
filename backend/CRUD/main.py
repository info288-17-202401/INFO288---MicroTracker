import uvicorn
import logging
# from app.core.Settings import settings
from dotenv import load_dotenv
from os import getenv

import sys
# def setup_logging():
#     logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
load_dotenv()
try:
    PORT = int(getenv("PORT"))
    HOST = str(getenv("HOST"))
except Exception as e:
    print("Error al cargar las variables de entorno")
    HOST = "0.0.0.0"
    PORT = 4000

def run_app():
    uvicorn.run(app="app.app:app", port=PORT, host=HOST, loop='asyncio', log_level='debug', reload=True)

if __name__ == "__main__":
    # setup_logging()  # Configurar el registro antes de ejecutar la aplicación
    run_app()