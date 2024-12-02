from datetime import datetime, timedelta, timezone
from jose import JWTError
import jwt
from auth_modules.config import settings

def create_access_token(data: dict, expires_delta: timedelta = None): # A dict containing data to be encoded into JWT and timedelta specifier for how long token is valid
    to_encode = data.copy() # A copy of the data dictionary is made as to not modify the original input; Holds infomation used in JWT
    if expires_delta: # If expiration time proviced...
        expire = datetime.now(timezone.utc) + expires_delta # Calclate expire by adding time to curr time in UTC
    else: # if no expiration time proviced...
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Use default expiration time defined in Settings 
    to_encode.update({"exp": expire}) # The expiration time is added to the to_encode dict under the standard JWT "exp" field
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM) # Encode using secret key and algorithm used to sign the token
    return encoded_jwt # Encoded JWT can be used as an access token for authentication