# tests/conftest.py - VERSION AVEC AsyncMock
import pytest
import asyncio
import sys
import os
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime, timezone

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Définition des constantes de test
VALID_BCRYPT_HASH_1 = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_ID_1 = "507f1f77bcf86cd799439011"

# Fix for Windows async tests
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture
def mock_db():
    """Mock de la base de données MongoDB avec AsyncMock"""
    users_collection = AsyncMock()
    users_collection.find_one = AsyncMock(return_value=None)
    
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = TEST_USER_ID_1
    users_collection.insert_one = AsyncMock(return_value=mock_insert_result)
    
    db = AsyncMock()
    db.users = users_collection
    
    return db

@pytest.fixture
def test_user():
    return {
        "_id": TEST_USER_ID_1,
        "email": TEST_USER_EMAIL,
        "hashed_password": VALID_BCRYPT_HASH_1,
        "is_active": True,
        "created_at": "2023-01-01T00:00:00Z"
    }

@pytest.fixture
def client():
    """Client de test avec AsyncMock pour toutes les fonctions async"""
    from schemas.user import UserInDB
    
    # Créez un mock UserInDB
    mock_user_db = UserInDB(
        id=TEST_USER_ID_1,
        email=TEST_USER_EMAIL,
        hashed_password=VALID_BCRYPT_HASH_1,
        created_at=datetime.now(timezone.utc),
        is_active=True
    )
    
    # Patch toutes les fonctions async avec AsyncMock
    with patch('src.auth.crud.get_user_by_email', new_callable=AsyncMock) as mock_get_user:
        with patch('src.auth.crud.create_user_as_userindb', new_callable=AsyncMock) as mock_create_user:
            with patch('src.auth.crud.authenticate_user_as_userindb', new_callable=AsyncMock) as mock_auth_user:
                with patch('core.security.verify_password') as mock_verify:
                    with patch('core.security.create_access_token') as mock_token:
                        with patch('dependencies.auth.get_current_user', new_callable=AsyncMock) as mock_current_user:
                            # Configurez les mocks
                            mock_get_user.return_value = None
                            mock_create_user.return_value = mock_user_db
                            mock_auth_user.return_value = None
                            mock_verify.return_value = True
                            mock_token.return_value = "mocked-jwt-token"
                            mock_current_user.return_value = mock_user_db
                            
                            # Importez TOUS les routeurs
                            from routers.login import router as login_router
                            from routers.register import router as register_router
                            from routers.me import router as me_router
                            
                            # Créez l'application
                            app = FastAPI()
                            app.include_router(login_router)
                            app.include_router(register_router)
                            app.include_router(me_router)
                            
                            yield TestClient(app)