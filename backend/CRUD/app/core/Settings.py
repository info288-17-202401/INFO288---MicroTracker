from typing import (
    # Annotated, 
    Any, 
    # Literal, 
    Dict
    )
from pydantic import (
    PostgresDsn,
    # computed_field,
)
# from pydantic_settings import SettingsConfigDict, BaseSettings
from dotenv import load_dotenv
from os import getenv
import logging
from app.core.utils import getJsonFile

logging.basicConfig(level=logging.DEBUG)

def SQLALCHEMY_DATABASE_URL(user, password, server, port, db) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=user,
            password=password,
            host=server,
            port=port,
            path=db,
        )

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings():
    def __init__(self, configfile: str) -> None:
        logging.debug(f"Loading settings from {configfile}")
        self.config_file = configfile
        # BACKEND_CORS_ORIGINS: Annotated[INFO288-BibliotecaDigitalDistribuida/databases/db.py
        #     list[AnyUrl] | str, BeforeValidator(parse_cors)
        # ] = []
        # ID: int = int(getenv("ID"))
           
        json_file: Dict[str, Any] = getJsonFile(self.config_file)

        load_dotenv()
        self.ID : int = int(json_file["ID"])
        self.LINES_IDS: list[int] = json_file["LINES_IDS"]
        # POSTGRES_DB: str = str(getenv("POSTGRES_DB"))
        # POSTGRES_PORT: int = int(getenv("POSTGRES_PORT"))
        self.POSTGRES_DB: str = str(json_file["POSTGRES_DB"])
        self.POSTGRES_PORT: int = json_file["POSTGRES_PORT"]
        self.POSTGRES_USER: str = str(getenv("POSTGRES_USER"))
        # POSTGRES_SERVER: str = str(getenv("POSTGRES_SERVER"))
        self.POSTGRES_SERVER: str = json_file["POSTGRES_SERVER"]
        self.POSTGRES_PASSWORD: str = str(getenv("POSTGRES_PASSWORD"))
        # TYPE: str = str(self.json_file["TYPE"])
        self.LOG_LEVEL: str = str(getenv("LOG_LEVEL"))
        self.SQLALCHEMY_DATABASE_URL : PostgresDsn = SQLALCHEMY_DATABASE_URL(self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_SERVER, self.POSTGRES_PORT, self.POSTGRES_DB)
    
    # model_config = SettingsConfigDict(
    #     env_file=".env", env_ignore_empty=True, extra="ignore"
    # )

    def __repr__(self) -> str:
        return f"Settings({self.dict()})"
    
database_1 = Settings("/app/app/core/database1.json")
database_2 = Settings("/app/app/core/database2.json") 