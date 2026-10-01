from fastapi import Depends, HTTPException, Query, Cookie,Response,APIRouter,UploadFile, status
from typing import Annotated,List,Optional
from dependencies.auth import get_current_user
from database.connection import get_db
from schemas.user import UserInDB
from datetime import datetime, timezone
from src.media.crud import create_media, get_media_list, get_media_by_id, get_file, getfiletype
from core.security import validate_image
from fastapi.responses import FileResponse
from bson import ObjectId
import os

router = APIRouter(prefix="/api/media", tags=["Media"])

@router.post("/upload")
async def upload_file(file: UploadFile,current_user: UserInDB = Depends(get_current_user)):
    if current_user is None:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must be logged in to perform this action"
        )
    else:
       
        try:
            mime = await validate_image(file)
            contents = file.file.read()
            media = await create_media(file.filename, current_user.id)
            os.makedirs(os.path.dirname(media.path), exist_ok=True)
            with open(media.path, 'wb') as f:
                f.write(contents)
        except HTTPException:
            raise  # let validation / client errors (e.g. invalid file type) through
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
        finally:
            file.file.close()
        return {"message": f"Successfully uploaded {file.filename}"}




@router.get("")
async def get_user_media(current_user : UserInDB = Depends(get_current_user)):

    return await get_media_list(current_user)


@router.get("/{media_id}")
async def get_media_file(media_id: str, current_user : UserInDB =Depends(get_current_user)):
    media = await get_media_by_id(media_id)

    if not media:
        raise HTTPException(status_code=404, detail="Not found")

    # Ownership check
    if media["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    file_path = get_file(media)

    return FileResponse(file_path)

@router.delete("/{media_id}")
async def delete_media(
    media_id: str,
    current_user=Depends(get_current_user)
):
    db = get_db()
    try:
        oid = ObjectId(media_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Media not found")
    media = await db.media.find_one({"_id": oid})

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    # Ownership check
    if media["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Build file path
    file_path = os.path.join(
        "src",
        "media",
        "uploads",
        f"{media_id}{getfiletype(media['filename'])}"
    )

    # Delete file if exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete from DB
    await db.media.delete_one({"_id": oid})

    return {"message": "Media deleted successfully"}