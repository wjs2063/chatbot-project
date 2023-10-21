from typing import *
import os
from dotenv import load_dotenv,find_dotenv
from sqlalchemy import URL
load_dotenv(find_dotenv())

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR : str = "/api/v1"
    DB_USER : str = os.getenv("POSTGRES_USER","postgres")
    DB_PASSWORD : str = os.getenv("POSTGRES_PASSWORD","psql")
    _BARD_API_KEY : str = os.environ["_BARD_API_KEY"]
    _GPT_API_KEY : str = os.environ["_GPT_API_KEY"]
    POSTGRES_SCHEME : str = "postgresql+asyncpg"
    POSTGRES_SERVER : str =  "172.19.0.2" # 사설 IP 
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD : str = "postgres"
    POSTGRES_DB : str = "postgres"
    POSTGRES_PORT : str = "5432"
    ASYNC_SQLALCHEMY_DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    print(ASYNC_SQLALCHEMY_DATABASE_URL)
    """
    SQLALCHEMY_DATABASE_URL : "driver://[USER]:[PASSWORD]@[SERVER]:[PORT]/[DATABASE] 형식"
    "postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase"
    
    작성 -> dialect+driver://username:password@host:port/database
    """

    @field_validator("ASYNC_SQLALCHEMY_DATABASE_URL",mode = "before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return URL.create(
            "postgresql+asyncpg",
            username=os.getenv("POSTGRES_USER","postgres"),
            password=os.getenv("POSTGRES_PASSWORD","psql"),
            host=os.getenv("POSTGRES_SERVER","localhost"),
            database=os.getenv("POSTGRES_DB","test")
        )

    class Config:
        case_sensitive = True


settings = Settings()
