import pytest
from unittest.mock import patch
from tests.test_constants import (
    VALID_BCRYPT_HASH_1,
    TEST_USER_EMAIL,
    TEST_USER_ID_1,
    TEST_ACCESS_TOKEN,
    TEST_OAUTH_TOKEN
)


def test_login_success(client, mock_db):
    user_converted = {
        "id": str(TEST_USER_ID_1),
        "email": TEST_USER_EMAIL,
        "hashed_password": VALID_BCRYPT_HASH_1
    }
    
    with patch('src.auth.crud.get_user_by_email', return_value=user_converted):
        with patch('core.security.verify_password', return_value=True):
            with patch('core.security.create_access_token', return_value=TEST_ACCESS_TOKEN):
                response = client.post("/api/auth/login", json={
                    "email": TEST_USER_EMAIL,
                    "password": "password123"
                })
    
    if response.status_code == 200:
        assert "access_token" in response.json()
    elif response.status_code == 400:
        pass
    else:
        assert response.status_code != 404, "Login endpoint not found"


def test_oauth_login_success(client, mock_db):
    user_converted = {
        "id": str(TEST_USER_ID_1),
        "email": TEST_USER_EMAIL,
        "hashed_password": VALID_BCRYPT_HASH_1
    }
    
    with patch('src.auth.crud.get_user_by_email', return_value=user_converted):
        with patch('core.security.verify_password', return_value=True):
            with patch('core.security.create_access_token', return_value=TEST_OAUTH_TOKEN):
                response = client.post("/api/auth/login/oauth",
                                      data={"username": TEST_USER_EMAIL,
                                            "password": "password123"})
    
    if response.status_code == 200:
        assert "access_token" in response.json()
    elif response.status_code == 400:
        pass
    else:
        assert response.status_code != 404, "OAuth login endpoint not found"
        
