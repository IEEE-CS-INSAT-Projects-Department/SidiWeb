# tests/test_exceptions.py
import pytest
from fastapi.testclient import TestClient
from core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    WeakPasswordException
)

def test_custom_exceptions_import():
    """Test que les exceptions personnalisées sont importables"""
    from core.exceptions import (
        InvalidCredentialsException,
        UserAlreadyExistsException,
        WeakPasswordException,
        UserNotFoundException,
        InactiveUserException
    )
    assert True  # Si on arrive ici, l'import a réussi

def test_exception_status_codes():
    """Test que les exceptions ont les bons codes de statut"""
    exc = InvalidCredentialsException()
    assert exc.status_code == 401
    
    exc = UserAlreadyExistsException()
    assert exc.status_code == 400
    
    exc = WeakPasswordException()
    assert exc.status_code == 400