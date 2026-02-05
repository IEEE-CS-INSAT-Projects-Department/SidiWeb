from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

#Schema for user creation/registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(...)

# Schema for user output/response
class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: Optional[datetime] = None

# Schema for user login (input from client)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: str  
    email: EmailStr
    hashed_password: str  
    created_at: datetime
    is_active: bool = True
    email_verified: bool = False
    last_login: Optional[datetime] = None
    role: str = "user"
    
    # Pydantic v2 config
    model_config = ConfigDict(
        from_attributes=True,  # Previously 'orm_mode'
        protected_namespaces=()  # Avoid conflicts with Python keywords
    )
    
    # Create UserInDB from MongoDB document
    @classmethod
    def from_mongo_document(cls, mongo_doc: dict) -> "UserInDB":
        return cls(
            id=str(mongo_doc.get("_id", "")),
            email=mongo_doc.get("email", ""),
            hashed_password=mongo_doc.get("hashed_password", ""),
            created_at=mongo_doc.get("created_at", datetime.now(timezone.utc)),
            is_active=mongo_doc.get("is_active", True),
            email_verified=mongo_doc.get("email_verified", False),
            last_login=mongo_doc.get("last_login"),
            role=mongo_doc.get("role", "user")
        )
