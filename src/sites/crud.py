from bson import ObjectId
from datetime import datetime


async def create_site(db, site_data: dict, user_id: str):
    site_data["owner_id"] = user_id
    site_data["published"] = False
    site_data["public_url"] = None
    site_data["created_at"] = datetime.utcnow()

    result = await db.sites.insert_one(site_data)
    site_data["id"] = str(result.inserted_id)
    return site_data


async def get_user_sites(db, user_id: str):
    sites = []
    cursor = db.sites.find({"owner_id": user_id})
    async for site in cursor:
        site["id"] = str(site["_id"])
        sites.append(site)
    return sites


async def get_site_by_id(db, site_id: str):
    site = await db.sites.find_one({"_id": ObjectId(site_id)})
    if site:
        site["id"] = str(site["_id"])
    return site


async def update_site(db, site_id: str, update_data: dict):
    await db.sites.update_one(
        {"_id": ObjectId(site_id)},
        {"$set": update_data}
    )
    return await get_site_by_id(db, site_id)


async def delete_site(db, site_id: str):
    await db.sites.delete_one({"_id": ObjectId(site_id)})