from pydantic import BaseModel
from beanie import Document, Indexed
from FastAPI import UploadFile



class MediaOut(BaseModel):
    id: int
    user_id: int
    filename: str
    path: str
    uploaded_at: datetime

class Media(Document):
    #id: int
    filename: str
    path: str
    uploaded_at: datetime=(datetime.utcnow)
    user_id: int
