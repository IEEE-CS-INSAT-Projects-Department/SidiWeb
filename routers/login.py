from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserInDB
from schemas.token import TokenResponse
from src.auth.crud import get_user_by_email
from core.security import verify_password, create_access_token
from core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse,summary="Login with email and password",description="Authenticate user with email and password, returns JWT token",)
async def login(user_data: UserCreate) -> dict:
    """ Authenticate user and return access token """
    db_user = await get_user_by_email(user_data.email)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email",
        )
    if not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )
        
    token_data = {"sub": db_user.email}  
    access_token = create_access_token(token_data)
    expires_in_seconds = settings.access_token_expire_minutes * 60
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in_seconds,
    }


@router.post(
    "/login/oauth",
    response_model=TokenResponse,
    summary="OAuth2-compatible login",
    description="OAuth2 password grant flow - only username and password required",
)
async def login_oauth_simple(
    username: str = Form(..., description="Username or email"),
    password: str = Form(..., description="Password"),
) -> dict:
    """
    Simplified OAuth2 login that only requires username and password.
    """
    email = username 
    db_user = await get_user_by_email(email)
  
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or email",
        )
        
    if not verify_password(password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )
    
    token_data = {"sub": db_user.email}  
    access_token = create_access_token(token_data)
    expires_in_seconds = settings.access_token_expire_minutes * 60
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in_seconds,
    }


