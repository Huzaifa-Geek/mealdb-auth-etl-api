import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

# Config


SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = PasswordHasher()

def get_password_hash(password: str):
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    
    try:
        return pwd_context.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False


# JWT Token

def create_access_token(data: dict):
    to_encode = data.copy()
    
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )