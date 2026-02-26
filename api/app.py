"""
Flask API server for SidiWeb AI recommendations.
Port: 5001
"""
import sys
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from dotenv import load_dotenv

workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))
load_dotenv(workspace_root / ".env")

from src.chains.recommendation_chain import create_recommendation_chain
from api.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    ErrorResponse
)

app = Flask(__name__)
CORS(app)

print("🔧 Initializing AI recommendation chain...")
try:
    chain = create_recommendation_chain()
    print("✅ Chain initialized successfully")
except Exception as e:
    print(f"❌ Chain initialization failed: {e}")
    chain = None


@app.route("/", methods=["GET"])
def home():
    """API root endpoint."""
    return jsonify({
        "status": "running",
        "service": "SidiWeb AI Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /recommend": "Get AI recommendations"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "ai_chain_ready": chain is not None,
        "port": 5001
    })


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Main recommendation endpoint.
    
    Request:
        POST /recommend
        Body: {
            "category": "startup",
            "style": "moderne",
            "preferences": "tech, innovant"
        }
    
    Response:
        200: RecommendationResponse
        400: Bad request
        422: Validation error
        500: Server error
    """
    
    if chain is None:
        return jsonify({
            "success": False,
            "error": "AI chain not initialized",
            "detail": "Check API key in .env file (GOOGLE_API_KEY or OPENAI_API_KEY)"
        }), 500

    data = request.get_json()
    
    if data is None:
        return jsonify({
            "success": False,
            "error": "Bad request",
            "detail": "No JSON body provided or invalid JSON format"
        }), 400

    try:
        validated_request = RecommendationRequest(**data)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Validation error",
            "detail": str(e)
        }), 422

    try:
        print(f"\n📥 Request: {validated_request.category} / {validated_request.style}")
        
        result = chain.invoke(
            category=validated_request.category,
            style=validated_request.style,
            preferences=validated_request.preferences
        )
        
        print(f"✅ Generated successfully")
        
        response = {
            "success": True,
            "recommended_templates": result.get("recommended_templates", []),
            "recommended_palette": result.get("recommended_palette", {}),
            "recommended_fonts": result.get("recommended_fonts", {}),
            "fallback_used": result.get("_fallback_used", False)
        }
        
        return jsonify(response), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            "success": False,
            "error": "Recommendation generation failed",
            "detail": str(e)
        }), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({
        "success": False,
        "error": "Bad request",
        "detail": str(error)
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "detail": "Check API documentation for valid endpoints"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "success": False,
        "error": "Method not allowed",
        "detail": "Check the HTTP method (GET/POST)"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "detail": str(error)
    }), 500


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  SIDIWEB AI - FLASK API SERVER")
    print("=" * 70)
    print(f"  🚀 Starting server...")
    print(f"  📍 URL: http://localhost:5001")
    print(f"  📍 Health: GET http://localhost:5001/health")
    print(f"  📍 Recommend: POST http://localhost:5001/recommend")
    print("=" * 70 + "\n")
    
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )


# Export ASGI app for uvicorn while preserving Flask local run above.
# This keeps `uvicorn app:app --port 5001 --reload` working.
flask_app = app
app = FastAPI()
app.mount("/", WSGIMiddleware(flask_app))
