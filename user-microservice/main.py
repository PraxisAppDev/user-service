from fastapi import FastAPI, HTTPException                                      # Import FastAP framework and HTTPException for error handling
from database import RedisClient
from service import UserService                                                 # Import the UserService class to manage user ops
from schemas import UserUpdate, UserCreate, UserResponseModel
from event_listener import UserEventListener # Import he UserEventListenerf
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    listener_task = loop.create_task(start_event_listener())

    yield # application keeps running while event listener runs in background

    # shutdown logic
    listener_task.cancel() # cancel task  on shutdown

# /// MOVE TO SCHEMAS ///
# User listens for these events and processes them asynchronously
app = FastAPI(lifespan=lifespan) # Initialize FastAPI application instance
redis_client = RedisClient()
user_service = UserService()    # Create an instance of UserService for handling user-related logic


async def start_event_listener():
    listener = UserEventListener() # init event listener
    await listener.listen_for_events() # listen for events from redis streams

@app.get("/ping")
def ping_redis():
    if redis_client.test_conn():
        return {"msg": "Redis connection success"}
    else:
        raise HTTPException(status_code=500, detail="Redis connection fail")
    
@app.post("/users/")
def create_user(user: UserCreate):
    try:
        # Call the userService to create a new user
        # I think you would hash the password here eventually?
        user_service.create_user(user.username, user.password, user.phone, user.email)
        return {"msg": "User created Successfully"}  # Return success message when user created successfully
    except ValueError as e:
        # If valueError raised (e.g., user already exists), return 400 bad request error
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/users/{username}")
def update_user(username: str, user_update: UserUpdate):
    try:
        user_service.update_user(username, user_update.model_dump(exclude_unset=True))
        return {"msg": "User Updated Successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/users/login")
def login_user(username:str, password: str):
    try:
        # Attempt to log the user in via UserService's login_user method
        user = user_service.login_user(username, password)
        # Return a success message along with user's data
        return {"msg": "login successful", "user": user.to_dict()}
    except ValueError as e:
        # If login fails (e.g., wrong password), return a 400 Bad Request with the error
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{username}")
def delete_user(username: str):
    try:
        # Call the delete_user method from UserService
        user_service.delete_user(username)
        return {"msg": f"User {username} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/users/getall")
def get_all_users():
    users = user_service.get_all_users()
    return users

@app.get("/users/id", response_model=UserResponseModel)
def get_user_by_id(username:str, password: str):
    user = user_service.login_user(username, password) #TODO: MAKE ACCESS TO ONE USER INSTANCE
    curr_user_id = user.id
    print(curr_user_id)
    user = user_service.find_user_by_id(curr_user_id)
    if user:
        return UserResponseModel(
            message="User deleted successfully",
            content={}
        )
    else:
        raise HTTPException(status_code=404, detail=f"User not found")

if __name__=="__main__":
    import uvicorn  # Import Uvicorn for running the FastAPI application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # Run the FastAPI application with Uvicorn on port 8000