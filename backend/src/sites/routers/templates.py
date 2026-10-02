from fastapi import APIRouter, Depends, HTTPException
from typing import List
from database.connection import get_db
from src.sites.schemas.templateOut import TemplateOut
from src.sites import crud

router = APIRouter(prefix="/api/templates", tags=["Templates"])


@router.get("", response_model=List[TemplateOut])
async def list_templates(db=Depends(get_db)):
    return await crud.get_templates(db)


@router.get("/{template_id}", response_model=TemplateOut)
async def get_template(template_id: str, db=Depends(get_db)):
    template = await crud.get_template_by_id(db, template_id)

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    return template
