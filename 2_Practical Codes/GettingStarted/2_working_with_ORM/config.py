from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    jwt_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    

    # Tells Pydantic to read variables from the .env file
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()