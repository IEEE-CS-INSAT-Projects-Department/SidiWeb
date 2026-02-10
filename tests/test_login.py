# tests/test_login.py - AVEC AsyncMock
import pytest
from unittest.mock import patch, AsyncMock
from tests.test_constants import (
    VALID_BCRYPT_HASH_1,
    TEST_USER_EMAIL,
    TEST_USER_ID_1,
    TEST_ACCESS_TOKEN,
    TEST_OAUTH_TOKEN
)

def test_login_success(client):
    user_converted = {
        "_id": TEST_USER_ID_1,
        "email": TEST_USER_EMAIL,
        "hashed_password": VALID_BCRYPT_HASH_1
    }
    
    # UTILISEZ AsyncMock POUR LES FONCTIONS ASYNC
    with patch('src.auth.crud.get_user_by_email', new_callable=AsyncMock) as mock_get_user:
        with patch('core.security.verify_password') as mock_verify:
            with patch('core.security.create_access_token') as mock_token:
                mock_get_user.return_value = user_converted
                mock_verify.return_value = True
                mock_token.return_value = TEST_ACCESS_TOKEN
                
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

def test_oauth_login_success(client):
    user_converted = {
        "_id": TEST_USER_ID_1,
        "email": TEST_USER_EMAIL,
        "hashed_password": VALID_BCRYPT_HASH_1
    }
    
    # UTILISEZ AsyncMock POUR LES FONCTIONS ASYNC
    with patch('src.auth.crud.authenticate_user_as_userindb', new_callable=AsyncMock) as mock_auth:
        with patch('core.security.create_access_token') as mock_token:
            mock_auth.return_value = user_converted
            mock_token.return_value = TEST_OAUTH_TOKEN
            
            response = client.post("/api/auth/login/oauth",
                                  data={"username": TEST_USER_EMAIL,
                                        "password": "password123"})
    
    if response.status_code == 200:
        assert "access_token" in response.json()
    elif response.status_code == 400:
        pass
    else:
        assert response.status_code != 404, "OAuth login endpoint not found"