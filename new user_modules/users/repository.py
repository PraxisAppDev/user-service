import redis
import redis.asyncio
import redis.asyncio.client
from users.model import UserModel
import uuid

class UserRepository:
    def __init__(self):
        # Initialize async Redis client (Redis cloud settings)
        self.redis_client = redis.asyncio.client.Redis(host="redis-12893.c8.us-east-1-4.ec2.redns.redis-cloud.com",port=12893,password="hAlZdUs2811tjwgZhohkG9E1XSMNBkSu", db=0,decode_responses=True)
    async def add_user(self, user: UserModel) -> str:
        user_id = str(uuid.uuid4())
        user.hash_password() # Hash the password before storing
        user_data = user.model_dump(exclude={"password"}) # Store all user data except password
        user_data["password_hash"] = user.password # Store the hashed password separately
        user_data['id'] = user_id # Set generated IF in the user data (temp fix)
        await self.redis_client.hset(user_id, mapping=user_data) # Store user data in Redis
        return user_id
    
    async def test_conn(self):
        try:
            await self.redis_client.ping()
            return True
        except redis.ConnectionError:
            return False

    async def user_exists(self, username: str) -> bool:
        return await self.redis_client.exists(f"user:{username}") > 0

    # New method to retrieve all users (debugging purposes only!)
    async def get_all(self):
        keys = await self.redis_client.keys("user:*") # Get all user keys
        users = []
        for key in keys:
            user_data = await self.redis_client.hgetall(key) # Retrieve the data for each user
            users.append(user_data)
        return users
    
    # Asynchronously update user data in Redis
    async def update_user(self, username: str, update_data: dict) -> bool:
        user_id = f"user:{username}"
        if await UserRepository.user_exists(user_id):
            await self.redis_client.hmset(user_id, update_data)
            return True
        return False
    
    async def delete_user(self, username: str) -> bool:
        user_id = f"user:{username}"
        if await UserRepository.user_exists(user_id):
            await self.redis_client.delete(user_id)
            return True
        return False
    
    async def get_user_by_id(self, user_id: str):
        # Retrieve user data from Redis based on username
        user_data = await self.redis_client.hgetall(user_id)
        if user_data:
            return user_data
        return None
repository = UserRepository()