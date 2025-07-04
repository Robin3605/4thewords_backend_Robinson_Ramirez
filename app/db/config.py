from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_link: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()