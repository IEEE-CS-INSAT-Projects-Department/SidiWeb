from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/")
async def auth_root():
    return {"message": "Auth module active"}