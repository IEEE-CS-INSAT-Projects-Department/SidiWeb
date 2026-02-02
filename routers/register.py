from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserCreate, UserOut
from src.auth.crud import get_user_by_email, create_user
from core.security import verify_password, create_access_token
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(user.email, user.password)
    return {
        "id": new_user["id"],
        "email": new_user["email"],
        "created_at": new_user["created_at"]
    }