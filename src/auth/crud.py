from database.connection import user_collection
from datetime import datetime
from core.security import hash_password

async def get_user_by_email(email: str):
    return await user_collection.find_one({"email": email})

async def create_user(email: str, password: str):
    hashed = hash_password(password)
    user_data = {
        "email": email,
        "hashed_password": hashed,
        "created_at": datetime.utcnow()
    }
    result = await user_collection.insert_one(user_data)
    user_data["id"] = str(result.inserted_id)
    return user_data
