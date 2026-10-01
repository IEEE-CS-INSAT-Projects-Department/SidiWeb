# schemas/user.py - VERSION COMPLÈTEMENT CORRIGÉE
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator

# Schema for user creation/registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)  # CRITIQUE: min_length=1
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        # Cette validation ne s'exécutera PAS pour les chaînes vides
        # car min_length=1 empêche déjà les chaînes vides
        
        # Vérifier si c'est seulement des espaces
        if v.isspace():
            raise ValueError('Password cannot be only whitespace')
        
        # Vérifier la longueur (déjà fait par Field, mais double vérification)
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        
        if len(v) > 128:
            raise ValueError('Password cannot exceed 128 characters')
        
        # Vérifier si c'est seulement numérique
        if v.isnumeric():
            raise ValueError('Password cannot be only numeric')
        
        return v

# Schema for user output/response
class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: Optional[datetime] = None

# Schema for user login (input from client)
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)  # CRITIQUE: min_length=1

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
        from_attributes=True,
        protected_namespaces=()
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