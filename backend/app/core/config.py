from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Starter Pro 2"
    POSTGRES_URL: str = Field(
        default="postgresql+asyncpg://psp_user:psp_pass@localhost:5432/psp",
        description="PostgreSQL database URL"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    SECRET_KEY: str = Field(
        default="replace_this_key",
        description="JWT secret key"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        description="JWT token expiration in minutes"
    )

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.REDIS_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.REDIS_URL

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

