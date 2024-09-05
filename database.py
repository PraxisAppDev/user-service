import redis
import json                     # Import JSON module for serialization and deserialization of data
from model import UserModel     # Import UserModel class for creating and retrieving user objects

class RedisClient:
    def __init__(self, host='', port=11734, db=0, password=''):
        # Initialize Redis client with connection details (host, port, db, password, decode_responses)
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
    
    def test_conn(self):
        try:
            self.client.ping()
            return True
        except redis.ConnectionError:
            return False

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