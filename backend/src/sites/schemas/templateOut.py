from pydantic import BaseModel
from typing import Optional, Any, Dict


class TemplateOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    structure: Optional[Dict[str, Any]] = None
