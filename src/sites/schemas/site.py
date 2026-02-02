from pydantic import BaseModel
from typing import list , Optional
from datetime import datetime


class sitesection(BaseModel):
    accueil : str
    contact : str



class sitecontent(BaseModel):
    section : sitesection



class site ( BaseModel):
    id : str
    owner_id :str
    template_id: str
    name : str
    content : sitecontent
    created_at : datetime
    updated_at: Optional[datetime]=None