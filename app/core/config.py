from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "FASTAPI MVC"
    ROOT_PATH: str = ""
    
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 1010
    
    DBUSERNAME: str
    DBPASSWORD: str
    DBNAME: str
    ALGORITHM: str
    
    
    class Config:
        env_file = ".env"

settings = Settings()