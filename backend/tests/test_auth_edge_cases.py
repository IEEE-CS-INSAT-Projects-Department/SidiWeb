# tests/test_auth_edge_cases.py - VERSION COMPLÈTEMENT CORRIGÉE
import pytest
import time
from unittest.mock import patch
from datetime import datetime, timezone

def test_login_invalid_email(client):
    """Test avec email invalide"""
    with patch('routers.login.get_user_by_email') as mock_get_user:
        mock_get_user.return_value = None
        
        response = client.post("/api/auth/login", json={
            "email": "wrong@email.com",
            "password": "wrongpass"
        })
        
        assert response.status_code == 400
        assert "Invalid email" in response.json()["detail"]

def test_login_invalid_password(client, test_user):
    """Test avec mot de passe invalide"""
    with patch('routers.login.get_user_by_email') as mock_get_user:
        with patch('routers.login.verify_password') as mock_verify:
            mock_get_user.return_value = test_user
            mock_verify.return_value = False
            
            response = client.post("/api/auth/login", json={
                "email": test_user["email"],
                "password": "wrongpassword"
            })
            
            assert response.status_code == 400
            detail = response.json()["detail"].lower()
            assert "invalid" in detail or "password" in detail

def test_successful_login(client, test_user):
    """Test de connexion réussie"""
    with patch('routers.login.get_user_by_email') as mock_get_user:
        with patch('routers.login.verify_password') as mock_verify:
            with patch('routers.login.create_access_token') as mock_token:
                mock_get_user.return_value = test_user
                mock_verify.return_value = True
                mock_token.return_value = "mocked-jwt-token"
                
                response = client.post("/api/auth/login", json={
                    "email": test_user["email"],
                    "password": "testpassword123"
                })
                
                assert response.status_code == 200
                assert "access_token" in response.json()
                assert response.json()["token_type"] == "bearer"

def test_register_weak_password(client):
    """Test avec mot de passe trop faible"""
    with patch('routers.register.get_user_by_email') as mock_get_user:
        mock_get_user.return_value = None
        
        response = client.post("/api/auth/register", json={
            "email": "new@example.com",
            "password": "123"  # Trop court
        })
        
        # Pydantic valide -> 422 au lieu de 400
        assert response.status_code == 422
        errors = response.json().get("detail", [])
        # Vérifiez qu'il y a une erreur de validation
        assert len(errors) > 0

def test_register_numeric_password(client):
    """Test avec mot de passe uniquement numérique"""
    with patch('routers.register.get_user_by_email') as mock_get_user:
        mock_get_user.return_value = None
        
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "password": "12345678"  # Que des chiffres
        })
        
        # Pydantic valide -> 422 au lieu de 400
        assert response.status_code == 422
        errors = response.json().get("detail", [])
        # Vérifiez qu'il y a une erreur de validation
        assert len(errors) > 0

def test_register_existing_user(client):
    """Test d'inscription avec un email existant"""
    with patch('routers.register.get_user_by_email') as mock_get_user:
        # Simuler un utilisateur existant
        mock_get_user.return_value = {
            "_id": "507f1f77bcf86cd799439013",
            "email": "existing@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
        }
        
        response = client.post("/api/auth/register", json={
            "email": "existing@example.com",
            "password": "ValidPass123"  # Mot de passe valide
        })
        
        # Notre validation métier -> 400 (UserAlreadyExistsException)
        assert response.status_code == 400
        assert "already" in response.json()["detail"].lower()

@pytest.mark.parametrize("email,password,expected_status,expected_keyword", [
    ("", "Password123", 422, None),  # Email vide -> Pydantic 422
    ("invalid-email", "Password123", 422, None),  # Format email invalide -> Pydantic 422
    ("test@example.com", "", 422, None),  # Mot de passe vide -> Pydantic 422
    ("test@example.com", "123", 422, None),  # Mot de passe trop court -> Pydantic 422
    ("test@example.com", "a" * 129, 422, None),  # Mot de passe trop long -> Pydantic 422
    ("test@example.com", "12345678", 422, None),  # Mot de passe numérique -> Pydantic 422
    ("test@example.com", "Password123", 400, "already"),  # Utilisateur existant -> 400
])
def test_edge_case_inputs(client, email, password, expected_status, expected_keyword):
    """Tests de diverses entrées borderline"""
    with patch('routers.register.get_user_by_email') as mock_get_user:
        # Pour le dernier cas, simuler un utilisateur existant
        if email == "test@example.com" and password == "Password123":
            mock_get_user.return_value = {"_id": "123", "email": email}
        else:
            mock_get_user.return_value = None
        
        response = client.post("/api/auth/register", json={
            "email": email,
            "password": password
        })
        
        assert response.status_code == expected_status
        if expected_keyword and response.status_code == 400:
            assert expected_keyword in response.json()["detail"].lower()

def test_oauth_login_success(client):
    """Test OAuth2 login réussie"""
    from schemas.user import UserInDB
    
    mock_user = UserInDB(
        id="507f1f77bcf86cd799439011",
        email="test@example.com",
        hashed_password="hashed",
        created_at=datetime.now(timezone.utc),
        is_active=True
    )
    
    with patch('routers.login.authenticate_user_as_userindb') as mock_auth:
        with patch('routers.login.create_access_token') as mock_token:
            mock_auth.return_value = mock_user
            mock_token.return_value = "mocked-jwt-token"
            
            response = client.post("/api/auth/login/oauth", 
                data={
                    "username": "test@example.com",
                    "password": "password123"
                })
            
            assert response.status_code == 200
            assert "access_token" in response.json()

def test_oauth_login_invalid(client):
    """Test OAuth2 login avec identifiants invalides"""
    with patch('routers.login.authenticate_user_as_userindb') as mock_auth:
        mock_auth.return_value = None
        
        response = client.post("/api/auth/login/oauth", 
            data={"username": "wrong@email.com", "password": "wrong"})
        
        assert response.status_code in [400, 401]
        assert "invalid" in response.json()["detail"].lower()

def test_login_performance(client):
    """Test de performance sur /login"""
    with patch('routers.login.get_user_by_email') as mock_get_user:
        mock_get_user.return_value = None
        
        start = time.time()
        requests_count = 5
        
        for i in range(requests_count):
            response = client.post("/api/auth/login", json={
                "email": f"test{i}@example.com",
                "password": "wrongpassword"
            })
            assert response.status_code in [400, 401]
        
        duration = time.time() - start
        avg_time = duration / requests_count
        
        assert avg_time < 1.0

def test_debug_password_empty(client):
    """Test de débogage pour vérifier la validation Pydantic"""
    from schemas.user import UserInDB
    from datetime import datetime, timezone
    
    # Créez un mock UserInDB
    mock_user_db = UserInDB(
        id="507f1f77bcf86cd799439011",
        email="test@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        created_at=datetime.now(timezone.utc),
        is_active=True
    )
    
    with patch('routers.register.get_user_by_email') as mock_get_user:
        with patch('routers.register.create_user_as_userindb') as mock_create_user:
            mock_get_user.return_value = None
            mock_create_user.return_value = mock_user_db
            
            # Test avec mot de passe vide
            response = client.post("/api/auth/register", json={
                "email": "test@example.com",
                "password": ""
            })
            
            print(f"\nDEBUG - Mot de passe vide:")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            # Devrait être 422 (validation Pydantic)
            assert response.status_code == 422
            
            # Test avec mot de passe valide
            response = client.post("/api/auth/register", json={
                "email": "test@example.com",
                "password": "ValidPassword123"
            })
            
            print(f"\nDEBUG - Mot de passe valide:")
            print(f"Status: {response.status_code}")
            
            # Devrait être 201 (succès)
            assert response.status_code == 201