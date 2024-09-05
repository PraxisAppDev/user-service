from database import RedisClient    # RedisClient interacts with Redis
from model import UserModel         # Import UserModel class for creating user objects

class UserService:
    def __init__(self):
        self.db = RedisClient() # Initialize RedisClient instance for database operation 
    
    def create_user(self, username: str, password_hash: str, phone: str = None, email: str = None):
        # If a user with the same username exists already
        if self.db.get_user(username):
            raise ValueError("User already exists") # Raise error
        
        # Create new UserModel oject with username and password_hash
        user = UserModel(username, password_hash, phone, email)
        self.db.save_user(user) # Save new user to database