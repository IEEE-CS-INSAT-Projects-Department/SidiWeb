from database.connection import get_db
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from .schemas import Media
from schemas.user import UserInDB
import os


def getfiletype(filename):
    n=len(filename)
    for i in range(n-1,-1,-1):
        if filename[i]==".":
            return filename[i::]
    return ""
from datetime import datetime, timezone
from bson import ObjectId

def get_file_extension(filename: str) -> str:
    idx = filename.rfind(".")
    return filename[idx:] if idx != -1 else ""

async def create_media(filename: str, user_id: str) -> Media:
    db = get_db()
    ext = get_file_extension(filename)

    media_data = {
        "filename": filename,
        "uploaded_at": datetime.now(timezone.utc),
        "user_id": user_id,
        "path": "/temp/path"
    }

    result = await db.media.insert_one(media_data)
    media_data["_id"] = result.inserted_id
    media_data["path"] = f"src/media/uploads/{result.inserted_id}"+getfiletype(filename)
    query_filter = {"_id": media_data["_id"]}
    update_operation = {"$set": {"path": media_data["path"]}}
    await db.media.update_one(query_filter, update_operation)    
    return Media.from_mongo_document(media_data)

async def get_media_list(current_user : UserInDB):
 
    media_list = []
    async for media in get_db().media.find({"user_id": current_user.id}):
        media["_id"] = str(media["_id"])
        media_list.append(media)
    return media_list

async def get_media_by_id(media_id : str):
    return await get_db().media.find_one({"_id": ObjectId(media_id)})

def get_file(media : Media):
    print(os.system("pwd"))
    return os.path.join(
        "src",
        "media",
        "uploads",
        f"{media['_id']}{getfiletype(media['filename'])}"
    )
    