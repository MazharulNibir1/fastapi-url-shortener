from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener"
    redis_url: str = "redis://localhost:6379/0"
    class Config:
        env_file = ".env"

settings = Settings()