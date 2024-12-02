from fastapi import APIRouter, HTTPException
from users.service import service
from users.model import UserModel, UpdateUserModel
from users.repository import repository

router = APIRouter()

@router.get("/ping")
async def ping_redis():
    if await repository.test_conn():
        return {"msg": "Redis connection success"}
    else:
        raise HTTPException(status_code=500, detail="Redis connection fail")

@router.post("/add", status_code=201)
async def add_user(user: UserModel):
    user_id = await service.add_user(user)
    if user_id:
        return {"id": user_id}
    else:
        raise HTTPException(status_code=409, detail="User already exists") # Indicates a request conflict with the current state of a resource

# New endpoint to retrieve all users
@router.get("/get_all", status_code=200)
async def read_users():
    users = await service.get_users()
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="No users found")
    
@router.put("/update/{username}", status_code=200)
async def update_user(username: str, user_data: UpdateUserModel):
    updated = await service.update_user(username, user_data.model_dump(exclude=True))
    if updated:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.delete("/delete/{username}", status_code=200)
async def delete_user(username: str):
    deleted = await service.delete_user(username)
    if deleted:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.get("/users/{username}", status_code=200)
async def get_user_by_id(user_id: str):
    try:
        retrieved = await service.get_user_by_id(user_id)
        if retrieved:
            return retrieved
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))