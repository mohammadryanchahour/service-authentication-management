from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Secret key for encrypting and decrypting JWT tokens
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    
    # Algorithm used for encoding JWT tokens
    ALGORITHM: str = Field(..., env='ALGORITHM')
    
    # Access token expiration time in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')
    
    # Refresh token expiration time in minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(..., env='REFRESH_TOKEN_EXPIRE_MINUTES')
    
    # MongoDB URI for connecting to the MongoDB database
    MONGODB_URI: str = Field(..., env='MONGODB_URI')
    
    # URL for the User Management service
    USER_MANAGEMENT_SERVICE_URL: str = Field(..., env='USER_MANAGEMENT_SERVICE_URL')
    
    # URL for the Redis instance used for caching or session management
    REDIS_URL: str = Field(..., env='REDIS_URL')
    
    # Define the environment (e.g., development, production)
    ENVIRONMENT: str = Field('development', env='ENVIRONMENT')
    
    # Host and Port for running the FastAPI Authentication service
    HOST: str = Field('127.0.0.1', env='HOST')
    PORT: int = Field('8000', env='PORT')
    
    # Flag to determine if the application should reload (default is False)
    RELOAD: bool = Field(False, env='RELOAD')

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.ENVIRONMENT == "development":
            self.RELOAD = True

settings = Settings()
