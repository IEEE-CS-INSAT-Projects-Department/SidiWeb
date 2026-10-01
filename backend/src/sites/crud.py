import json
from pathlib import Path
from bson import ObjectId
from datetime import datetime

_TEMPLATES_DIR = Path(__file__).resolve().parent / "data"


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


# --- Templates (read-only, seeded from bundled JSON files) ---

async def seed_templates(db):
    """Load the bundled template JSON files into MongoDB once (if empty)."""
    if await db.templates.count_documents({}) > 0:
        return
    docs = []
    for path in sorted(_TEMPLATES_DIR.glob("template_*.json")):
        with path.open(encoding="utf-8") as f:
            docs.append(json.load(f))
    if docs:
        await db.templates.insert_many(docs)


def _serialize_template(doc: dict) -> dict:
    doc["id"] = doc.get("id") or str(doc["_id"])
    doc.pop("_id", None)
    return doc


async def get_templates(db):
    templates = []
    async for doc in db.templates.find({}):
        templates.append(_serialize_template(doc))
    return templates


async def get_template_by_id(db, template_id: str):
    doc = await db.templates.find_one({"id": template_id})
    if doc:
        return _serialize_template(doc)
    return None