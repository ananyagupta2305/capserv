# bot/settings.py
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CRM_BASE_URL: str = os.getenv("CRM_BASE_URL", "http://localhost:8001")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TRANSCRIPT_MAX_LEN: int = 1000

settings = Settings()
