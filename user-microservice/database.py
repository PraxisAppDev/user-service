import redis
import json                     # Import JSON module for serialization and deserialization of data
from model import UserModel     # Import UserModel class for creating and retrieving user objects

class RedisClient:
    def __init__(self, host='your-redis-host', port=11734, db=0, password='your-redis-pw'):
        # Initialize Redis client with connection details (host, port, db, password, decode_responses)
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
    #///DEBUGGING///
    def test_conn(self):
        try:
            self.client.ping()
            return True
        except redis.ConnectionError:
            return False
        
    
    def get_all(self):
        # Find all keys that match the user pattern in Redis
        user_keys = self.client.keys("user:*")

        # users = [
        #     # fetch each user's data from Redis and deserialize it
        #     json.loads(await self.client.get(key))
        #     for key in user_keys
        # ]

        # # Return the list of users
        # return list(map(lambda document: document, users))

        # Fetch all user data using keys
        users = []
        for key in user_keys:
            user_data = self.client.get(key)
            if user_data:
                # Convert the user data back to a dictionary and append to the users list
                users.append(UserModel.from_dict(json.loads(user_data)))
        return users
    #///DEBUGGNG///
    def save_user(self, user: UserModel):
        # Serialize UserModel object to JSON string and save it in Redis
        self.client.set(f"user:{user.username}", json.dumps(user.to_dict()))
    
    def get_user(self, username: str):
        # Retrieve user data from Redis based on the username
        user_data = self.client.get(f"user:{username}")
        if user_data:
            # Deserialize JSON string to dict and create UserModel object
            return UserModel.from_dict(json.loads(user_data))
        return None # Return None if user does not exist
    
    def delete_user(self, username: str):
        # Remove the user from Redis using the username as the key
        self.client.delete(f"user:{username}")

    # def find_one_by_id(self, user_id: str):
    #     user = self.client.(f"id:{user_id}")
    #     if user:
    #         #user.pop("password_hash", None) # Remove sensitive data
    #         return UserModel.from_dict(json.loads(user))
    #     return None
    
    # async def find_one_by_email(self, email: str):
    #     user_id = await self.client.get(f"email:{email}")
    #     if user_id:
    #         return await self.find_one_by_id(user_id)
    #     return None