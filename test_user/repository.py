import redis
import redis.asyncio.client
from model import UserModel, UserCreate
#import uuid
import json
import hashlib

class UserRepository:
    def __init__(self):
        # Here, Redis Cloud is used for simplicity sake; The plan was to eventually run the redis database from a docker container and connect to it that way. this wouldnt incure costs
        self.redis_client = redis.asyncio.client.Redis(host="your-redis-host-here",port=12893,password="your-pw-here", db=0,decode_responses=True)


    async def add_user(self, user: UserCreate):
        print("2")
        new_user = UserModel(user)
        new_user.to_dict
        print(new_user["username"])
        new_user["password_hash"] = self.hash_password(user.password)        
        await self.redis_client.set(new_user["id"], json.dumps(new_user)) # Store user data as a Redis hash
        print(new_user)
    
    async def get_user(self, username: str):
        user_data = await self.redis_client.get(f"username: {username}")
        print(username)
        if not user_data:
            return None
        print("1")
        return UserModel.from_dict(json.loads(user_data))
    
    # async def get_all_users(self):
    #     users = []
    #     async for user_id in self.redis_client.scan_iter(): # Iterate over keys
    #         user_data = await self.redis_client.hgetall(user_id)
    #         if user_data:
    #             users.append(UserModel.from_dict(user_data))
    #     return users

    async def get_all(self):
        # Find all keys that match the user pattern in Redis
        user_keys = self.redis_client.keys("user:*")
        users = []
        for key in user_keys:
            user_data = self.redis_client.get(key)
            if user_data:
                # Convert the user data back to a dictionary and append to the users list
                users.append(UserModel.from_dict(json.loads(user_data)))
        return users

    # Method to hash the user's password
    def hash_password(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest
    
repository = UserRepository()
