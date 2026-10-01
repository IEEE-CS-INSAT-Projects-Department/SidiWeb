from pydantic import BaseModel
from fastapi import UploadFile
from datetime import datetime, timezone



class MediaOut(BaseModel):
    id: str
    user_id: str
    filename: str
    path: str
    uploaded_at: datetime


class Media(BaseModel):
    id: str
    filename: str
    path: str
    uploaded_at: datetime
    user_id: str

    @classmethod
    def from_mongo_document(cls, mongo_doc: dict) -> "Media":
        return cls(
            id=str(mongo_doc.get("_id", "")),
            uploaded_at=mongo_doc.get("uploaded_at", datetime.now(timezone.utc)), 
            filename=mongo_doc.get("filename", ""),
            path=mongo_doc.get("path", ""),
            user_id=mongo_doc.get("user_id", "")
        )


