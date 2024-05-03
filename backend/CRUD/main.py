import uvicorn
from app.core.Settings import settings

def run_app():
    uvicorn.run(app="app.app:app", port=settings.PORT, host=settings.HOST, loop='asyncio', log_level='info', reload=True)

if __name__ == "__main__":
    run_app()