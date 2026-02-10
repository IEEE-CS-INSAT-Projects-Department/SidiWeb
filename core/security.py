# core/security.py - CORRIGEZ create_access_token
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional, Dict, Any
from core.config import settings
from core.exceptions import TokenExpiredException, TokenInvalidException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

hash_password = get_password_hash

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire})
    
    # CORRECTION: Utilisez le bon nom d'attribut
    # Regardez dans config.py quel est le nom exact
    # S'il y a une erreur, essayez l'une de ces options:
    try:
        # Option 1: Essayer avec jwt_secret_key
        secret_key = settings.jwt_secret_key
    except AttributeError:
        try:
            # Option 2: Essayer avec secret_key
            secret_key = settings.secret_key
        except AttributeError:
            # Option 3: Essayer avec JWT_SECRET_KEY
            secret_key = settings.JWT_SECRET_KEY
    
    encoded_jwt = jwt.encode(
        to_encode, 
        secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    try:
        # Même logique pour la clé secrète
        try:
            secret_key = settings.jwt_secret_key
        except AttributeError:
            try:
                secret_key = settings.secret_key
            except AttributeError:
                secret_key = settings.JWT_SECRET_KEY
                
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except jwt.JWTError:
        raise TokenInvalidException()