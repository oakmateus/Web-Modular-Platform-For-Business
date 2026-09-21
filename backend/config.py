from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    access_token_secret_key: str
    access_token_expire_minutes: int
    refresh_token_secret_key: str
    refresh_token_expire_days: int
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()