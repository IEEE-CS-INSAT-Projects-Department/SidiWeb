import json
import unicodedata
from pathlib import Path
from typing import Dict, List

import httpx
from fastapi import APIRouter

from core.config import settings
from schemas.recommendations import AIRecommendationRequest, AIRecommendationResponse

router = APIRouter(prefix="/api", tags=["AI Recommendations"])

_DESIGN_SYSTEM_PATH = Path(__file__).resolve().parent.parent / "data" / "design_system.json"


def _normalize(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return ascii_value.strip().lower()


def _load_design_system() -> dict:
    with _DESIGN_SYSTEM_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _build_category_templates_map(design_system: dict) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for template in design_system.get("templates", []):
        category = _normalize(template.get("category", ""))
        template_id = template.get("id")
        if not category or not template_id:
            continue
        result.setdefault(category, []).append(template_id)
    return result


def _build_style_categories_map(design_system: dict) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    style_mappings = design_system.get("style_mappings", {})
    for style, categories in style_mappings.items():
        normalized_style = _normalize(style)
        normalized_categories = [_normalize(cat) for cat in categories if cat]
        if normalized_categories:
            result[normalized_style] = normalized_categories
    return result


def _build_palette_by_category_map(design_system: dict) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for palette in design_system.get("color_palettes", []):
        category = _normalize(palette.get("category", ""))
        palette_id = palette.get("id")
        if category and palette_id and category not in result:
            result[category] = palette_id
    return result


def _build_font_by_category_map(design_system: dict) -> Dict[str, dict]:
    result: Dict[str, dict] = {}
    for pairing in design_system.get("font_pairings", []):
        font_payload = {
            "heading": pairing.get("heading", ""),
            "body": pairing.get("body", ""),
            "reason": pairing.get("description", "Fallback readable font pair"),
        }
        for raw_category in pairing.get("categories", []):
            category = _normalize(raw_category)
            if category and category not in result:
                result[category] = font_payload
    return result


_DESIGN_SYSTEM = _load_design_system()
_CATEGORY_TEMPLATES = _build_category_templates_map(_DESIGN_SYSTEM)
_STYLE_CATEGORIES = _build_style_categories_map(_DESIGN_SYSTEM)
_PALETTE_BY_CATEGORY = _build_palette_by_category_map(_DESIGN_SYSTEM)
_FONT_BY_CATEGORY = _build_font_by_category_map(_DESIGN_SYSTEM)

_ALL_TEMPLATE_IDS: List[str] = [
    t.get("id") for t in _DESIGN_SYSTEM.get("templates", []) if t.get("id")
]
_ALL_PALETTE_IDS: List[str] = [
    p.get("id") for p in _DESIGN_SYSTEM.get("color_palettes", []) if p.get("id")
]
_ALL_FONTS: List[dict] = [
    {
        "heading": f.get("heading", ""),
        "body": f.get("body", ""),
        "reason": f.get("description", "Fallback readable font pair"),
    }
    for f in _DESIGN_SYSTEM.get("font_pairings", [])
    if f.get("heading") and f.get("body")
]


def _build_recommend_url() -> str:
    base_url = (settings.ia_api_url or "http://127.0.0.1:5001").rstrip("/")
    if base_url.endswith("/recommend"):
        return base_url
    return f"{base_url}/recommend"


def _resolve_category(category: str, style: str) -> str:
    normalized_category = _normalize(category)
    if normalized_category in _CATEGORY_TEMPLATES:
        return normalized_category

    normalized_style = _normalize(style)
    for candidate_category in _STYLE_CATEGORIES.get(normalized_style, []):
        if candidate_category in _CATEGORY_TEMPLATES:
            return candidate_category

    if _CATEGORY_TEMPLATES:
        return next(iter(_CATEGORY_TEMPLATES.keys()))
    return ""


def _build_fallback(payload: AIRecommendationRequest, error_message: str) -> AIRecommendationResponse:
    category = _resolve_category(payload.category, payload.style)

    templates = _CATEGORY_TEMPLATES.get(category, [])
    if not templates:
        templates = _ALL_TEMPLATE_IDS[:2]

    if len(templates) == 1:
        templates = [templates[0], templates[0]]

    palette = _PALETTE_BY_CATEGORY.get(category)
    if not palette and _ALL_PALETTE_IDS:
        palette = _ALL_PALETTE_IDS[0]

    fonts = _FONT_BY_CATEGORY.get(category)
    if not fonts and _ALL_FONTS:
        fonts = _ALL_FONTS[0]

    fonts = fonts or {
        "heading": "",
        "body": "",
        "reason": "Fallback readable font pair",
    }

    return AIRecommendationResponse(
        success=True,
        recommended_templates=[
            {
                "id": templates[0],
                "reason": f"Fallback template for category '{payload.category}' from data/design_system.json",
            },
            {
                "id": templates[1] if len(templates) > 1 else templates[0],
                "reason": "Fallback alternative template",
            },
        ],
        recommended_palette={
            "id": palette,
            "reason": f"Fallback palette from data/design_system.json for category '{category or payload.category}'",
        },
        recommended_fonts=fonts,
        fallback_used=True,
        source="fallback",
        upstream_error=error_message,
    )


@router.post(
    "/recommendations",
    response_model=AIRecommendationResponse,
    summary="Proxy IA recommendations",
    description="Proxifie la requête vers le service IA local et applique un fallback en cas d'erreur.",
)
async def proxy_recommendations(payload: AIRecommendationRequest) -> AIRecommendationResponse:
    target_url = _build_recommend_url()
    timeout = httpx.Timeout(16.0, connect=4.0)
    print(f"[recommendations-proxy] POST -> {target_url}")

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(target_url, json=payload.model_dump())
            response.raise_for_status()
            data = response.json()

        return AIRecommendationResponse(
            success=bool(data.get("success", True)),
            recommended_templates=data.get("recommended_templates", []),
            recommended_palette=data.get("recommended_palette", {}),
            recommended_fonts=data.get("recommended_fonts", {}),
            fallback_used=bool(data.get("fallback_used", False)),
            source="ai",
            upstream_error=None,
        )

    except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError, ValueError) as exc:
        print(f"[recommendations-proxy] upstream error: {exc}")
        return _build_fallback(payload, str(exc))
