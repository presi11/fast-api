
  
from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    TITLE: str = Field(..., env="WEP_APP_TITLE")
    VERSION: str = Field(..., env="WEB_APP_VERSION")
    DESCRIPTION: str = Field(..., env="WEP_APP_DESCRIPTION")
    ENVIRONMENT: str = Field(...)
 
    POSTGRES_DATABASE_URL: str = Field(..., env="POSTGRES_DATABASE_URL")

    DEFAULT_DATA: bool = Field(..., env="DEFAULT_DATA")
    DEFAULT_DEV_DATA: bool = Field(..., env="DEFAULT_DEV_DATA")

    DEFAULT_DELTA: int = Field(7)
   
    CELERY_BROKER: str = Field(..., env="CELERY_BROKER")
    CELERY_BACKEND: str = Field(..., env="CELERY_BACKEND")
    
@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()


settings = get_settings()