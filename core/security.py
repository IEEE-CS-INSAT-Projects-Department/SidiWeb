from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import re
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BCRYPT_MAX_PASSWORD_LENGTH = 72

def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    if not re.search(r'[A-Z]', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter"
        )
    
    if not re.search(r'[a-z]', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter"
        )
    
    if not re.search(r'\d', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one digit"
        )
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
        )
        
def hash_password(password: str) -> str:
    validate_password_strength(password)
    truncated_password = password[:BCRYPT_MAX_PASSWORD_LENGTH]
    return pwd_context.hash(truncated_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    try:
        # Create a copy to avoid modifying the original data
        to_encode = data.copy()
        
        # Calculate expiration time
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        
        # Add expiration claim
        to_encode.update({"exp": expire})
        
        # Encode the JWT token
        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    except JWTError as e:
        # Re-raise with more context
        raise JWTError(f"Failed to create access token: {str(e)}") from e