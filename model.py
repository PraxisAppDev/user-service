from datetime import datetime   # Impoer datatime for handling timestamps

class UserModel:
    def __init__(self, username, password_hash):
        self.username = username                        # Store username
        self.password_hash = password_hash              # Store hashed password
        self.created_at = datetime.now().isoformat()    # Store creation time in ISO format

    def to_dict(self):
        # Convert UserModel object to dict for serialization
        return{
            "username": self.username,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        # Create UserModel object from dict (used when retrieving data from Redis)
        return cls(
            username=data["username"],
            password_hash=data["password_hash"],
        )