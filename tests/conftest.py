import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test constants
from tests.test_constants import (
    VALID_BCRYPT_HASH_1,
    VALID_BCRYPT_HASH_2,
    VALID_BCRYPT_HASH_3,
    VALID_BCRYPT_HASH_4,
    TEST_USER_EMAIL,
    TEST_USER_EMAIL_2,
    TEST_USER_EMAIL_3,
    TEST_USER_PASSWORD,
    TEST_USER_PASSWORD_2,
    TEST_USER_PASSWORD_3,
    TEST_USER_ID_1,
    TEST_USER_ID_2,
    TEST_USER_ID_3,
    TEST_JWT_TOKEN,
    TEST_ACCESS_TOKEN,
    TEST_OAUTH_TOKEN
)

# Fix for Windows async tests
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def event_loop():
    # Create event loop for async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

# Mock MongoDB database
@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.users = AsyncMock()
    db.users.find_one = AsyncMock(return_value=None)
    db.users.insert_one = AsyncMock()
    return db

# Test user data
@pytest.fixture
def test_user():
    return {
        "_id": TEST_USER_ID_1,
        "email": TEST_USER_EMAIL,
        "hashed_password": VALID_BCRYPT_HASH_1,
    }

# Another test user
@pytest.fixture
def test_user_2():
    return {
        "_id": TEST_USER_ID_2,
        "email": TEST_USER_EMAIL_2,
        "hashed_password": VALID_BCRYPT_HASH_2,
    }


@pytest.fixture
def valid_user_data():
    return {
        "email": TEST_USER_EMAIL_3,
        "password": TEST_USER_PASSWORD_3
    }


@pytest.fixture
def existing_user():
    return {
        "_id": TEST_USER_ID_3,
        "email": "existing@example.com",
        "hashed_password": VALID_BCRYPT_HASH_3,
    }


# Create FastAPI test client with mocked database
@pytest.fixture
def client(mock_db):
    with patch('database.connection.get_db', return_value=mock_db):
        with patch('src.auth.crud.get_db', return_value=mock_db):
            app = FastAPI()

            try:
                from routers.me import router as me_router
                app.include_router(me_router)
            except ImportError as e:
                print(f"Note: me router not found - {e}")
            
            try:
                from routers.login import router as login_router
                app.include_router(login_router)
            except ImportError as e:
                print(f"Note: login router not found - {e}")
            
            try:
                from routers.register import router as register_router
                app.include_router(register_router)
            except ImportError as e:
                print(f"Note: register router not found - {e}")
            
            # Add a test route to verify app is working
            @app.get("/test-ping")
            async def test_ping():
                return {"message": "Test app is working"}
            
            return TestClient(app)


# Additional helper fixtures
# Create authentication headers
@pytest.fixture
def auth_headers():
    def _create_headers(token: str):
        return {"Authorization": f"Bearer {token}"}
    return _create_headers


# Return a mock user in the format get_user_by_email returns
@pytest.fixture
def mock_user_dict():
    return {
        "id": str(TEST_USER_ID_1),
        "email": TEST_USER_EMAIL,
        "hashed_password": VALID_BCRYPT_HASH_1,
    }
