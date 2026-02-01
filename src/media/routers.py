from fastapi import Depends, HTTPException, Query, Cookie,Response,APIRouter
from typing import Annotated,List,Optional

router = APIRouter()

@router.post("/api/media/upload")
def upload_file():
    pass
