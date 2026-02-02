from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: str
    email: EmailStr
    hashed_password: str
    created_at: datetime

class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
