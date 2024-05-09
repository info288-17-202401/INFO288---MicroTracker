import uvicorn
import logging
from app.core.Settings import settings
import sys
# def setup_logging():
#     logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run_app():
    uvicorn.run(app="app.app:app", port=settings.PORT, host=settings.HOST, loop='asyncio', log_level='debug', reload=True)

if __name__ == "__main__":
    # setup_logging()  # Configurar el registro antes de ejecutar la aplicación
    run_app()