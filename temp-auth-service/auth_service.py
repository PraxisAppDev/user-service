from fastapi import FastAPI, Depends, HTTPException, status
import gen_key
import jwt
import redis
from passlib.context import CryptContext

app = FastAPI()

SECRET_KEY = gen_key.secret
ALGORITHM = "HS256"

from fastapi.security import OAuth2PasswordBearer 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# redis_client = redis.StrictRedis(
#     host="redis-11734.c11.us-east-1-3.ec2.redns.redis-cloud.com",
#     port=11734,
#     password="zMJq8dQ7IQhh4ooxREeEDinaqCK8NS9q",
#     db=0,
#     decode_responses=True
# )

# class tokenData(BaseModel):
#     user_id: str | None = None # Pydantic model for token data


# Publish event when user logs in or is authenticated
class AuthEventPublisher:
    def __init__(self, host='your-redis-host', port=11734, db=0, password='your-redis-pw', stream_key='auth_to_user_stream'):
        # Initialize Redis client with connection details (host, port, db, password, decode_responses)
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
        self.stream_key = stream_key

    def publish_event(self, user_id: str):
        event = {
            'type': 'user_authenticated',
            'user_id': user_id
        }
        self.client.xadd(self.stream_key, event)

# # Method to extract current user ID from JWT token
# def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
#     # Here, you would decode the token and extract the user ID
#     # you would do this using a JWT token for example:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub") # Extract user ID from the "sub" claim

#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token does not contain user ID",
#                 headers={"www-Authenticate": "Bearer"},
#             )
        
#         # Publish the authentication event to Redis
#         publisher = AuthEventPublisher()
#         publisher.publish_event(user_id)  # Publish user authentication event

#         return {user_id}
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"www-Authenticate": "Bearer"},
#         )

#TODO THIS SHOULD QUERY DATABASE. MOCK FOR ILLUSTRATION
def get_user_from_database(username: str):
    fake_user_db = {
        "test_user": {"id": "user123", "username": "test_user", "password_hash": pwd_context.hash("test_password")}
    }
    return fake_user_db.get(username)

def authenticate_user(username: str, password: str):
    user_data = get_user_from_database(username)
    
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Verify password
    if not pwd_context.verify(password, user_data['password_hash']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    # Generate JWT token with user_id as 'sub' in payload
    token = jwt.encode({"sub": user_data['id']}, SECRET_KEY, algorithm=ALGORITHM)
    
    # Publish the event that the user authenticated successfully
    publisher = AuthEventPublisher()
    publisher.publish_event(user_data['id'])
    
    return {"token": token, "user_id": user_data['id']}  # Return token and user_id

# FastAPI login route
@app.post("/login/")
def login_user(username: str, password: str):
    return authenticate_user(username, password)

if __name__=="__main__":
    import uvicorn  # Import Uvicorn for running the FastAPI application
    uvicorn.run("auth_service:app", host="0.0.0.0", port=8001, reload=True) # Run the FastAPI application with Uvicorn on port 8000