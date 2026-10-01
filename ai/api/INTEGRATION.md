# Flask AI API - Integration Info

## Server

**URL:** `http://localhost:5001`  
**Startup:** `python api/app.py`

---

## Endpoints

### GET /

API info and available endpoints

**Response:**

```json
{
  "status": "running",
  "service": "SidiWeb AI Recommendation API",
  "version": "1.0.0",
  "endpoints": {
    "GET /": "API information",
    "GET /health": "Health check",
    "POST /recommend": "Get AI recommendations"
  }
}
```

---

### GET /health

Check if server is ready before calling `/recommend`

**Response:**

```json
{
  "status": "healthy",
  "ai_chain_ready": true,
  "port": 5001
}
```

---

### POST /recommend\*\*

### Request

```json
{
  "category": "startup",
  "style": "moderne",
  "preferences": "tech, innovant"
}
```

- `category` (required): string
- `style` (required): string
- `preferences` (optional): string

### Response 200

```json
{
  "success": true,
  "recommended_templates": [{ "id": "template_name", "reason": "..." }],
  "recommended_palette": {
    "id": "palette_name",
    "reason": "..."
  },
  "recommended_fonts": {
    "heading": "Font Name",
    "body": "Font Name",
    "reason": "..."
  },
  "fallback_used": false
}
```

### Errors

```json
{
  "success": false,
  "error": "Error type",
  "detail": "Description"
}
```

**Status codes:** 400 (bad request), 422 (validation), 500 (server error)

---

## Notes

- CORS enabled
- Response time: 2-5s (LLM processing)
- `fallback_used: true` = AI unavailable, used rule-based fallback
- Health check: `GET /health`
