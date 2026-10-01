import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers.recommendations import router


def _build_client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_recommendations_proxy_success(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "success": True,
                "recommended_templates": [{"id": "startup_tech", "reason": "AI reason"}],
                "recommended_palette": {"id": "tech_gradient", "reason": "AI palette"},
                "recommended_fonts": {
                    "heading": "Space Grotesk",
                    "body": "Work Sans",
                    "reason": "AI fonts",
                },
                "fallback_used": False,
            }

    class MockAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, *args, **kwargs):
            return MockResponse()

    monkeypatch.setattr("routers.recommendations.httpx.AsyncClient", MockAsyncClient)

    client = _build_client()
    response = client.post(
        "/api/recommendations",
        json={"category": "startup", "style": "moderne", "preferences": "tech"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["fallback_used"] is False
    assert body["source"] == "ai"
    assert body["recommended_templates"][0]["id"] == "startup_tech"


def test_recommendations_proxy_timeout_fallback(monkeypatch):
    class MockAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, *args, **kwargs):
            raise httpx.TimeoutException("upstream timeout")

    monkeypatch.setattr("routers.recommendations.httpx.AsyncClient", MockAsyncClient)

    client = _build_client()
    response = client.post(
        "/api/recommendations",
        json={"category": "startup", "style": "moderne", "preferences": "tech"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["fallback_used"] is True
    assert body["source"] == "fallback"
    assert body["upstream_error"]
