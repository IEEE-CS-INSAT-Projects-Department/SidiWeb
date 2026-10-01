from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime


class SiteCreate(BaseModel):
    name: str
    template_id: Optional[str] = None
    content: Optional[Dict[str, Any]] = None


class SiteUpdate(BaseModel):
    name: Optional[str] = None
    template_id: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    published: Optional[bool] = None


class SiteOut(BaseModel):
    id: str
    name: str
    template_id: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    published: bool = False
    public_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
