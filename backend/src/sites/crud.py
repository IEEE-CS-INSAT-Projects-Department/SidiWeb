import json
from pathlib import Path
from uuid import uuid4
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

_TEMPLATES_DIR = Path(__file__).resolve().parent / "data"


def _to_object_id(site_id: str):
    """Return an ObjectId or None if the string is not a valid id."""
    try:
        return ObjectId(site_id)
    except (InvalidId, TypeError):
        return None


def _block(block_type: str, data: dict) -> dict:
    return {"id": str(uuid4()), "type": block_type, "data": data}


def blocks_from_template(template: dict) -> list:
    """Build editable starter blocks from a template's structure."""
    structure = template.get("structure") or {}
    pages = structure.get("pages") or []
    features = structure.get("features") or []

    blocks = [_block("heading", {"text": template.get("name", "My site")})]
    if template.get("description"):
        blocks.append(_block("paragraph", {"text": template["description"]}))

    for page in pages:
        if str(page).strip().lower() in ("contact",):
            continue
        blocks.append(_block("heading", {"text": str(page)}))
        blocks.append(_block("paragraph", {"text": f"Content for the \"{page}\" section…"}))

    wants_contact = any("contact" in str(x).lower() for x in list(pages) + list(features))
    if wants_contact:
        blocks.append(_block("contact", {"title": "Contact us"}))

    return blocks


async def create_site(db, site_data: dict, user_id: str):
    site_data["owner_id"] = user_id
    site_data["published"] = False
    site_data["public_url"] = None
    site_data["created_at"] = datetime.utcnow()

    # Seed editable content from the chosen template when none was provided
    if not site_data.get("content") and site_data.get("template_id"):
        template = await get_template_by_id(db, site_data["template_id"])
        if template:
            site_data["content"] = {"blocks": blocks_from_template(template)}

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
    oid = _to_object_id(site_id)
    if oid is None:
        return None
    site = await db.sites.find_one({"_id": oid})
    if site:
        site["id"] = str(site["_id"])
    return site


async def update_site(db, site_id: str, update_data: dict):
    oid = _to_object_id(site_id)
    if oid is None:
        return None
    await db.sites.update_one(
        {"_id": oid},
        {"$set": update_data}
    )
    return await get_site_by_id(db, site_id)


async def delete_site(db, site_id: str):
    oid = _to_object_id(site_id)
    if oid is None:
        return
    await db.sites.delete_one({"_id": oid})


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