# Provides health check and aggregates all authentication endpoints.
from fastapi import APIRouter


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get(
    "/",
    summary="Authentication module status",
    description="Check if authentication module is active and get module information",
)
async def get_auth_module_status() -> dict:
    return {
        "message": "Authentication module is active",
        "module": "auth",
        "status": "operational",
        "endpoints": [
            "/api/auth/register",
            "/api/auth/login", 
            "/api/auth/login/oauth",
            "/api/auth/me",
        ],
    }