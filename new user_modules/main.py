from fastapi import FastAPI
from users.router import router as user_router

# Initialize FastAPI app
app = FastAPI(
    title="User Service",
    description="Microservice for user profile management",
)

# Include the user router to handle all user-related endpoints
app.include_router(user_router, prefix="/users", tags=["users"])

# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "User Service is running"}

if __name__ == "__main__":
    import uvicorn # Import Uvicorn for running the FastAPI application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
