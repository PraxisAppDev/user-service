from database import RedisClient    # RedisClient interacts with Redis
from model import UserModel         # Import UserModel class for creating user objects
from temp_auth_service import AuthService
from datetime import datetime
import hashlib

class UserService:
    def __init__(self):
        self.db = RedisClient() # Initialize RedisClient instance for database operation
        self.temp_auth_service = AuthService() # Initialize the AuthService for password verification
    
    # Method creates a new user and stores them in Redis
    def create_user(self, username: str, password: str, phone: str = None, email: str = None):
        # If a user with the same username exists already
        if self.db.get_user(username):
            raise ValueError("User already exists") # Raise error
        
        # Create new UserModel oject with username and password
        password_hash = self.hash_password(password) # Hash password before saving
        new_user = UserModel(username, password_hash, phone, email)
        self.db.save_user(new_user) # Save new user to database
        
        # Old user object creation
        # user = UserModel(username, password_hash, phone, email)
        # self.db.save_user(user) # Save new user to database

    # Method updates user details (password, phone, email)
    def update_user(self, username, update_data: dict):
        user = self.db.get_user(username) # Fetch user from Redis
        # Check if username is in database
        if not user:
            raise ValueError("User does not exist")
        
        # Check for specific fields in update_data and update user accordingly
        if "password" in update_data:
            user.password_hash = self.hash_password(update_data["password"])
        if "phone" in update_data:
            user.phone = update_data["phone"]
        if "email" in update_data:
            user.email = update_data["email"]

        # Save updated user back to redis
        self.db.save_user(user)

    # Use AuthService to verify the provided password against the stored hash
    def login_user(self, username: str, password: str):
        user = self.db.get_user(username) # Get the user from Redis
        if not user:
            raise ValueError("User does not exist")
        
        # Verify the password using AuthService
        if not self.temp_auth_service.verify_password(password, user.password_hash):
            raise ValueError("Incorrect password")
        
        # set last login time
        user.last_login = datetime.now().isoformat()
        self.db.save_user(user)

        return user # Return user data after successful login
    
    def hash_password(self, password):
        # Demonstation hash
        return hashlib.sha256(password.encode()).hexdigest()
    
    def delete_user(self, username: str):
        user = self.db.get_user(username)
        if not user:
            raise ValueError("User does not exist")
        
        # If the user exists, remove them from Redis
        self.db.delete_user(username)

    def get_all_users(self):
        return self.db.get_all()
    
    def find_user_by_id(self, user_id):
        user = self.db.find_one_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    
    # def update_user_by_id(self, user_id, update_data: dict):
    #     user= self.find_user_by_id(user_id)
    #     if not user:
    #         raise ValueError("User does not exist")
        
    #     if "password" in update_data:
    #         user.password_hash = self.hash_password(update_data["password"])
    #     if "phone" in update_data:
    #         user.phone = update_data["phone"]
    #     if "email" in update_data:
    #         user.email = update_data["email"]

    #     self.db.save_user(user)
    #     return user
    
    # def delete_user_by_id(self, user_id):
    #     user = self.find_user_by_id(user_id)
    #     if not user:
    #         raise ValueError("User does not exist")
    #     self.db.delete_user(user_id)