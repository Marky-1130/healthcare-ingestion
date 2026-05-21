from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_ENDPOINT_URL: str
    S3_BUCKET: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

class Config:
    env_file = ".env"

settings = Settings()