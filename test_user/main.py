from fastapi import FastAPI
from router import router as user_router

app = FastAPI()

# Register the users router
app.include_router(user_router, prefix="/users")
# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "User Service is running"}

if __name__ == "__main__":
    import uvicorn # Import Uvicorn for running the FastAPI application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)