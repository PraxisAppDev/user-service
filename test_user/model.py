from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
import uuid
import hashlib

# Password hashing context using bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel:
    def __init__(self, username, password, email=None):
        self.id = str(uuid.uuid4())
        self.username = username    # Store username
        self.password = password    # store password
        self.email = email
    # id: Optional[str] = Field(default=None)
    # username: str
    # email: EmailStr
    # password: str
    
    def to_dict(self):
        return {
            #"id": self.id if self.id else str(uuid.uuid4), # Generate UUID if not present
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            #id=data.get("id"),
            username=data.get("username"),
            password=data.get("password"),
            email=data.get("email")
        )

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "testuser",
                    "email": "testuser@gmail.com",
                    "password": "strongpassword"
                }
            ]
        }
    }
