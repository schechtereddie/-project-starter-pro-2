from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Starter Pro 2"
    POSTGRES_URL: str = "postgresql+asyncpg://psp_user:psp_pass@localhost:5432/psp"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL

settings = Settings()

