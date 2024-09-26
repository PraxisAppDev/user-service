from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from constants import PHONE_REGEX
import re

class UserCreate(BaseModel):
    # Define the data model for user creation requests using Pydantic BaseModel
    username: str   # The username of the new user
    password: str   # The plaintext password of the new user
    phone: str = None
    email: EmailStr = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "test",
                    "password": "testpassword",
                    "phone": "123-456-7890",
                    "email": "test@gmail.com"
                }
            ]
        }
    }

    @field_validator('phone')
    def validate_phone(cls, phone):
        if phone and not re.match(PHONE_REGEX, phone):
            raise ValueError('Invalid phone number format')
        return phone

class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=6)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator('phone')
    def validate_phone(cls, phone):
        if phone and not re.match(PHONE_REGEX, phone):
            raise ValueError('Invalid phone number format')
        return phone
    
class UserResponseModel(BaseModel):
    message: str
    content: dict