from datetime import datetime   # Impoer datatime for handling timestamps
import uuid


class UserModel:
    def __init__(self, username, password_hash, phone=None, email=None):
        self.id = str(uuid.uuid4())                         # Generate a UUID for the user
        self.username = username                            # Store username
        self.password_hash = password_hash                  # Store hashed password
        self.phone = phone
        self.email = email
        self.created_at = datetime.now().isoformat()        # Store creation time in ISO format
        self.last_login = None

    def to_dict(self):
        # Convert UserModel object to dict for serialization
        return{
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at,
            "last_login": self.last_login,
        }

    @classmethod
    def from_dict(cls, data):
        # Create UserModel object from dict (used when retrieving data from Redis)
        instance = cls(
            username=data["username"],
            password_hash=data["password_hash"],
            phone=data.get("phone"),
            email=data.get("email")
        )
        # Safely assign `id` field, generating a new one if its missing
        instance.id = data.get("id", str(uuid.uuid4()))
        instance.created_at = data.get("created_at", datetime.now().isoformat())
        instance.last_login = data.get("last_login")
        return instance