from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserCreate, UserOut
from src.auth.crud import get_user_by_email, create_user
from core.security import verify_password, create_access_token
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login")
async def login(user: UserCreate):
    db_user = await get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer", "expires_in": 86400}
