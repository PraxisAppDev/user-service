from passlib.context import CryptContext
from fastapi import HTTPException
from auth_modules.utils import create_access_token
import requests
from datetime import timedelta
from auth_modules.config import settings

# Password hashing context
# Schemes specifies supported hashing algorithm
# Deprecated handles deprecated algorithms
# "auto" allows verifying PWs hashed w/ older algorithms
# New PWs hashed with most secure
pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

class AuthService:
    # Hash PW
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    # Auth user (calling user service)
    async def authenticate_user(self, username: str, password: str):
        # Call user service get user data
        user_response = requests.get(f"http://localhost:")