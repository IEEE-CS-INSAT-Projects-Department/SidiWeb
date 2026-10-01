# routers/login.py - VERSION CORRIGÉE
from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate
from schemas.token import TokenResponse
from src.auth.crud import get_user_by_email, authenticate_user_as_userindb  # Changez l'import
from core.security import verify_password, create_access_token
from core.config import settings
from core.exceptions import (
    InvalidCredentialsException, 
    InvalidEmailException, 
    InvalidPasswordException,
    InactiveUserException
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/login", 
    response_model=TokenResponse,
    summary="Login with email and password",
    description="Authenticate user with email and password, returns JWT token"
)
async def login(user_data: UserCreate) -> dict:
    """
    Authenticate user with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns access token with expiration time.
    """
    # Vérifier les identifiants — message générique pour éviter l'énumération d'emails
    db_user = await get_user_by_email(user_data.email)

    if not db_user or not verify_password(
        user_data.password, db_user.get("hashed_password", "")
    ):
        raise InvalidCredentialsException()
    
    # Vérifier si l'utilisateur est actif
    if not db_user.get("is_active", True):
        raise InactiveUserException()
        
    # Créer le token JWT
    token_data = {"sub": db_user["email"], "user_id": str(db_user["_id"])}
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
    description="OAuth2 password grant flow - uses form data (username=email, password)"
)
async def login_oauth_simple(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """
    OAuth2 compatible login endpoint.
    
    Uses standard OAuth2 password grant flow.
    - **username**: User's email address
    - **password**: User's password
    
    Returns access token with expiration time.
    """
    # Authentifier l'utilisateur
    user = await authenticate_user_as_userindb(form_data.username, form_data.password)
    
    if not user:
        raise InvalidCredentialsException()
    
    # Vérifier si l'utilisateur est actif
    if not user.is_active:
        raise InactiveUserException()
    
    # Créer le token JWT
    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(token_data)
    expires_in_seconds = settings.access_token_expire_minutes * 60
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in_seconds,
    }

# Optionnel: Endpoint pour rafraîchir le token
@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Refresh an expired access token using a refresh token"
)
async def refresh_token(refresh_token: str = Form(...)) -> dict:
    """
    Refresh an access token.
    
    - **refresh_token**: Valid refresh token
    
    Returns new access token.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not implemented yet"
    )