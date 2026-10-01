from pydantic import BaseModel
from typing import List

class templatecolour (BaseModel):
    primary : str
    secondary : str



class templatestructure(BaseModel):
    pages : List[str]
    layout: str
    colours : templatecolour
    features : List[str]



class template(BaseModel):
    id : str
    name : str
    description : str
    category : str
    structure : templatestructure 

