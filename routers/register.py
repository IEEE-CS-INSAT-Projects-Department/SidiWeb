from fastapi import APIRouter, HTTPException, status
from schemas.user import UserCreate, UserOut, UserInDB
from src.auth.crud import get_user_by_email, create_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user: UserInDB = await create_user(user_data.email, user_data.password)
    
    return UserOut(
        id=new_user.id,
        email=new_user.email,
        created_at=new_user.created_at,
        is_active=new_user.is_active
    )
    