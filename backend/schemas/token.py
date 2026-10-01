from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

#Schema for token response from login endpoints
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int



