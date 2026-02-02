from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserCreate, UserOut
from src.auth.crud import get_user_by_email, create_user
from core.security import verify_password, create_access_token
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "created_at": current_user["created_at"]
    }