from loguru import logger

from pydantic import BaseSettings, validator

class AppSettings(BaseSettings):
    DEBUG: bool
    HOST: str
    PORT: int

    SECRET: str

    BOT_TOKEN: str
    WEBHOOK_PATH: str
    WEBHOOK_URL: str

    PAYMENTS_PROVIDER_TOKEN: str

    ADMIN: int = 111


settings = AppSettings(_env_file='.env', _env_file_encoding='utf-8')
if settings.DEBUG:
    logger.debug(settings.dict())

