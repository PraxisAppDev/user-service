from fastapi import Depends, HTTPException, status
import hashlib

class AuthService:
    # Method checks if the provided plain password matches the hashed password
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        # Hash the plain password and compare it with the stored hashed password
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password