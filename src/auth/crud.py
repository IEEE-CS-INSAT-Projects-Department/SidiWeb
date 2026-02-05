from schemas.user import UserInDB
from database.connection import get_db
from datetime import datetime, timezone
from core.security import hash_password
from typing import Optional, Dict, Any

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    db = get_db()
    user_doc = await db.users.find_one({"email": email})
    
    if not user_doc:
        return None
    
    # Convert MongoDB document to UserInDB
    return UserInDB.from_mongo_document(user_doc)


async def create_user(email: str, password: str) -> UserInDB:
    db = get_db()
    hashed = hash_password(password)
    user_data = {
        "email": email,
        "hashed_password": hashed,
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
        "email_verified": False,
        "role": "user"
    }
    
    result = await db.users.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    
    # Return as UserInDB
    return UserInDB.from_mongo_document(user_data)