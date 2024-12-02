from fastapi import APIRouter, HTTPException
from model import UserCreate
from service import service

router = APIRouter()

@router.post("/add")
async def add_user(user: UserCreate):
    try:
        await service.add_user(user)
        return {"msg": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/all")
async def get_all_users():
    users = await service.get_all_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users