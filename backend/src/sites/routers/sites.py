from fastapi import APIRouter, Depends, HTTPException
from typing import List
from database.connection import get_db
from dependencies.auth import get_current_user
from schemas.user import UserInDB
from src.sites.schemas.site import SiteCreate, SiteUpdate, SiteOut
from src.sites import crud

router = APIRouter(prefix="/api/sites", tags=["Sites"])


@router.post("", response_model=SiteOut)
async def create_site(
    site: SiteCreate,
    db=Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    return await crud.create_site(db, site.dict(), current_user.id)


@router.get("", response_model=List[SiteOut])
async def list_sites(
    db=Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    return await crud.get_user_sites(db, current_user.id)


@router.get("/{site_id}", response_model=SiteOut)
async def get_site(
    site_id: str,
    db=Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    site = await crud.get_site_by_id(db, site_id)

    if not site:
        raise HTTPException(status_code=404, detail="Site introuvable")

    if site["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    return site


@router.put("/{site_id}", response_model=SiteOut)
async def update_site(
    site_id: str,
    site_update: SiteUpdate,
    db=Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    site = await crud.get_site_by_id(db, site_id)

    if not site:
        raise HTTPException(status_code=404, detail="Site introuvable")

    if site["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    update_data = site_update.dict(exclude_unset=True)

    if update_data.get("published"):
        update_data["public_url"] = f"https://sidiweb.com/{site_id}"

    return await crud.update_site(db, site_id, update_data)


@router.delete("/{site_id}")
async def delete_site(
    site_id: str,
    db=Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    site = await crud.get_site_by_id(db, site_id)

    if not site:
        raise HTTPException(status_code=404, detail="Site introuvable")

    if site["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    await crud.delete_site(db, site_id)

    return {"message": "Site deleted"}
