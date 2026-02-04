from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict, Field

class Settings(BaseSettings):    
    # App Settings 
    app_name: str = "SidiWeb Auth API"
    environment: str = "development"  
    
    # Database Settings
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "sidiweb_db"
    
    # Security/JWT Settings 
    jwt_secret_key: str  
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440 
    
    # Service Settings 
    fastapi_port: int  
    ia_api_url: str  
    upload_dir: str  
    
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore" )

settings = Settings()
