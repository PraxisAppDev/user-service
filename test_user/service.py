from model import UserModel, UserCreate
from repository import repository

class UserService:
    async def add_user(self, user: UserCreate):
        if await repository.get_user(user.username):
            raise ValueError("User already exists")
        return await repository.add_user(user)
    
    async def get_user_by_id(self, user_id: str):
        return await repository.get_user(user_id)
    
    async def get_all_users(self):
        return await repository.get_all()

service = UserService()
