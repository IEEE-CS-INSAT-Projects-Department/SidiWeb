from datetime import datetime, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import settings
from src.auth.crud import get_user_by_email_as_userindb
from schemas.user import UserInDB

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/oauth", auto_error=True)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB: 
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        user = await get_user_by_email_as_userindb(email)
        
        if user is None:
            raise credentials_exception
        
        return user  # Returns UserInDB object
    
    except JWTError:
        raise credentials_exception
    
    
