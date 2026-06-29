from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://matchday:matchday@localhost:5432/matchday"
    redis_url: str = "redis://localhost:6379/0"
    admin_api_token: str = "change-me-in-prod"

    class Config:
        env_file = ".env"


settings = Settings()
