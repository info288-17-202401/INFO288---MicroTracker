from typing import Annotated, Any, Literal, Dict
from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_settings import SettingsConfigDict, BaseSettings
from core import getJsonFileFromPath, SQLALCHEMY_DATABASE_URL


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=".env", env_ignore_empty=True, extra="ignore"
    # )
    json_file: Dict[str, Any] = getJsonFileFromPath()
    # BACKEND_CORS_ORIGINS: Annotated[
    #     list[AnyUrl] | str, BeforeValidator(parse_cors)
    # ] = []
    POSTGRES_PORT: int = str(json_file["POSTGRES_PORT"])
    POSTGRES_SERVER: str = str(json_file["POSTGRES_SERVER"])
    POSTGRES_USER: str = str(json_file["POSTGRES_USER"])
    POSTGRES_PASSWORD: str = str(json_file["POSTGRES_PASSWORD"])
    SLAVE_ID: int = json_file["SLAVE_ID"]
    POSTGRES_DB: str = json_file["POSTGRES_DB"]
    PORT: int = int(json_file["PORT"]) #Distinto del puerto de postgres
    TYPE: str = str(json_file["TYPE"])
    HOST: str = str(json_file["HOST"]) #
    
    SQLALCHEMY_DATABASE_URL : PostgresDsn = SQLALCHEMY_DATABASE_URL(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB)
    
    def __repr__(self) -> str:
        return f"Settings({self.model_config, self.DOMAIN, self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.HOST, self.MASTER_PORT, self.SQLALCHEMY_DATABASE_URL, self.BACKEND_CORS_ORIGINS, self.PORT, self.TYPE, self.json_file})"

settings = Settings() 