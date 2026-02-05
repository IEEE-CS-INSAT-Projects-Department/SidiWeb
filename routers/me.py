from fastapi import APIRouter, Depends
from schemas.user import UserOut, UserInDB  
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.get("/me", response_model=UserOut)
async def me(current_user: UserInDB = Depends(get_current_user)): 
    """Get current user info"""
    # Convert UserInDB to UserOut (Pydantic handles this automatically)
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        is_active=current_user.is_active,
        
    )