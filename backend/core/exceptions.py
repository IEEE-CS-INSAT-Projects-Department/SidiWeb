# core/exceptions.py
from fastapi import HTTPException, status


class AuthException(HTTPException):
    def __init__(self, detail: str = "Authentication error"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__(detail="Invalid email or password")


class InvalidEmailException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


class InvalidPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already registered",
        )


class WeakPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 8 characters",
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is disabled",
        )


class TokenExpiredException(AuthException):
    def __init__(self):
        super().__init__(detail="Your session has expired, please log in again")


class TokenInvalidException(AuthException):
    def __init__(self):
        super().__init__(detail="Invalid session, please log in again")
