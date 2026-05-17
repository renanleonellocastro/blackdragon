from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://blackdragon:blackdragon_dev@localhost:5432/blackdragon"
    SECRET_KEY: str = "change-me-in-production"
    FERNET_KEY: str = "change-me-in-production-must-be-32-bytes-base64-encoded="
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
