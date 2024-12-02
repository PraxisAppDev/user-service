# JWT configuration

import os
#from dotenv import load_dotenv # TODO: Hold secret in .env later
from gen_key import secret
from pydantic_settings import BaseSettings

# Load environment variables from a .env file
#load_dotenv()


class Settings(BaseSettings):
    #JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_default_secret")
    JWT_SECRET_KEY: str = secret
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # Token expiry time

settings = Settings()