# routers/register.py - VERSION FINALE SANS VALIDATION REDONDANTE
from fastapi import APIRouter, status
from schemas.user import UserCreate, UserOut
from src.auth.crud import get_user_by_email, create_user_as_userindb
from core.exceptions import UserAlreadyExistsException

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/register", 
    response_model=UserOut, 
    status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: UserCreate):
    """
    Register a new user.
    Toutes les validations de mot de passe sont faites par Pydantic dans UserCreate.
    """
    # Vérifier si l'utilisateur existe déjà
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise UserAlreadyExistsException()
    
    # Créer l'utilisateur (le mot de passe est déjà validé par Pydantic)
    new_user = await create_user_as_userindb(
        email=user_data.email,
        password=user_data.password
    )
    
    return UserOut(
        id=str(new_user.id),
        email=new_user.email,
        created_at=new_user.created_at
    )