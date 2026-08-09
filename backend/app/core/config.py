from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str= "RecruitIQ API"
    APP_VERSION: str="1.0.0"
    APP_ENV: str="development"
    DATABASE_URL: str

    SECRET_KEY: str 
    ALGORITHM: str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30
    GEMINI_API_KEY:str

    class Config:
        env_file=".env"

settings=Settings()