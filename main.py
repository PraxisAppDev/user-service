from fastapi import FastAPI, HTTPException  # Import FastAP framework and HTTPException for error handling
from database import RedisClient
from service import UserService             # Import the UserService class to manage user ops
from pydantic import BaseModel              # Import Basemodel from Pydantic to define request body models

app = FastAPI() # Initialize FastAPI application instance
redis_client = RedisClient()
user_service = UserService()    # Create an instance of UserService for handling user-related logic

class UserCreate(BaseModel):
    # Define the data model for user creation requests using Pydantic BaseModel
    username: str   # The username of the new user
    password: str   # The plaintext password of the new user

@app.get("/ping")
def ping_redis():
    if redis_client.test_conn():
        return {"msg": "Redis connection success"}
    else:
        raise HTTPException(status_code=500, detail="Redis connection fail")
    
@app.get("/users/")
def create_user(user: UserCreate):
    try:
        # Call the userService to create a new user
        # I think you would hash the password here eventually?
        user_service.create_user(user.username, user.password)
        return {"msg": "User created"}  # Return success message when user created successfully
    except ValueError as e:
        # If valueError raised (e.g., user already exists), return 400 bad request error
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__=="__main__":
    import uvicorn  # Import Uvicorn for running the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=5001) # Run the FastAPI application with Uvicorn on port 8000