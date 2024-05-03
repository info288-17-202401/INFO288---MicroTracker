from typing import Annotated, Any, Literal, Dict
from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_settings import SettingsConfigDict, BaseSettings
from dotenv import load_dotenv
from os import getenv
load_dotenv()

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

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    # json_file: Dict[str, Any] = getJsonFileFromPath()
    # BACKEND_CORS_ORIGINS: Annotated[INFO288-BibliotecaDigitalDistribuida/databases/db.py
    #     list[AnyUrl] | str, BeforeValidator(parse_cors)
    # ] = []
    ID: int = int(getenv("ID"))
    POSTGRES_DB: str = str(getenv("POSTGRES_DB"))
    POSTGRES_PORT: int = int(getenv("POSTGRES_PORT"))
    POSTGRES_USER: str = str(getenv("POSTGRES_USER"))
    POSTGRES_SERVER: str = str(getenv("POSTGRES_SERVER"))
    POSTGRES_PASSWORD: str = str(getenv("POSTGRES_PASSWORD"))
    PORT: int = int(getenv("PORT"))
    HOST: str = str(getenv("HOST"))
    # TYPE: str = str(json_file["TYPE"])
    
    SQLALCHEMY_DATABASE_URL : PostgresDsn = SQLALCHEMY_DATABASE_URL(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB)
    
    def __repr__(self) -> str:
        return f"Settings({self.model_config, self.DOMAIN, self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.HOST, self.MASTER_PORT, self.SQLALCHEMY_DATABASE_URL, self.BACKEND_CORS_ORIGINS, self.PORT, self.TYPE})"

settings = Settings() 