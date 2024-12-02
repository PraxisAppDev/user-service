from users.repository import repository
from users.model import UserModel

class UserService:
    # Asynchronoutly add user, ensuring no duplications
    async def add_user(self, user: UserModel) -> str:
        if await repository.user_exists(user.username):
            return None # User already exists
        return await repository.add_user(user)
    
    # New method to retrieve all users
    async def get_users(self):
        return await repository.get_all()
    
    async def get_user_by_id(self, user_id: str):
        if await repository.user_exists(user_id):
            return await repository.get_user_by_id(user_id)
        return None
    async def update_user(self, username: str, updated_data: dict) -> bool:
        # Hash the password if it's being updated
        if "password" in updated_data: 
            # Assuming we have the hash_password method implemented in UserModel
            updated_data["password_hash"] = UserModel.hash_password(updated_data.pop("password"))
        return await repository.update_user(username, updated_data)
    
    # Asynchronously delete a user
    async def delete_user(self, username: str) -> bool:
        return await repository.delete_user(username)
    
service = UserService()