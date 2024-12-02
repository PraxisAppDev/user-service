from typing import Optional
from pydantic import BaseModel, Field, EmailStr # TODO add email to requirements
from passlib.context import CryptContext

# Initialize password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model for profile-related data
class UserModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., write_only=True) # Password will be write-only (not returned in responses)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "email": "testuser@gmail.com",
                "password": "strongpassword123"
            }
        }
    
    # Method to hash the pasword before saving
    def hash_password(self):
        self.password = pwd_context.hash(self.password)

    # @classmethod
    # def from_dict(cls, data: dict):
    #     # Create UserModel object from dict (used when retrieving data from Redis)
    #     instance = cls(
    #         username=data["username"],
    #         email=data["email"],
    #         phone=data["phone"]
    #     )
    #     return instance


class UpdateUserModel(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]