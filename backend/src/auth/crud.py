# src/auth/crud.py - VERSION CORRIGÉE ET FINALE
from schemas.user import UserInDB
from database.connection import get_db
from datetime import datetime, timezone
from core.security import get_password_hash, verify_password
from typing import Optional, Dict, Any


def normalize_email(email: str) -> str:
    """Emails are case-insensitive; store and look them up in a canonical form."""
    return (email or "").strip().lower()


async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Get user by email from database.
    Returns raw MongoDB document (dict).
    """
    db =  get_db()
    user_doc = await db.users.find_one({"email": normalize_email(email)})
    return user_doc


async def get_user_by_email_as_userindb(email: str) -> Optional[UserInDB]:
    """
    Get user by email from database.
    Returns UserInDB model.
    """
    user_doc = await get_user_by_email(email)
    
    if not user_doc:
        return None
    
    # Convert MongoDB document to UserInDB
    return UserInDB.from_mongo_document(user_doc)


async def create_user(email: str, password: str) -> Dict[str, Any]:
    """
    Create a new user in database.
    Returns raw MongoDB document (dict).
    """
    db =  get_db()
    hashed = get_password_hash(password)
    user_data = {
        "email": normalize_email(email),
        "hashed_password": hashed,
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
        "email_verified": False,
        "role": "user"
    }
    
    result = await db.users.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    
    return user_data


async def create_user_as_userindb(email: str, password: str) -> UserInDB:
    """
    Create a new user in database.
    Returns UserInDB model.
    """
    user_data = await create_user(email, password)
    return UserInDB.from_mongo_document(user_data)


async def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with email and password.
    Returns user document if authentication succeeds, None otherwise.
    """
    user = await get_user_by_email(email)
    
    if not user:
        return None
    
    # Vérifier le mot de passe
    if not verify_password(password, user.get("hashed_password", "")):
        return None
    
    return user


# AJOUTEZ CETTE FONCTION - ELLE MANQUE !
async def authenticate_user_as_userindb(email: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate a user with email and password.
    Returns UserInDB if authentication succeeds, None otherwise.
    """
    user_doc = await authenticate_user(email, password)
    
    if not user_doc:
        return None
    
    return UserInDB.from_mongo_document(user_doc)


# Helper function to convert MongoDB document
def convert_mongo_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MongoDB document for API response.
    """
    if not doc:
        return None
    
    result = doc.copy()
    # Convert ObjectId to string
    if "_id" in result:
        result["id"] = str(result["_id"])
        del result["_id"]
    
    # Remove sensitive data
    if "hashed_password" in result:
        del result["hashed_password"]
    
    return result

    