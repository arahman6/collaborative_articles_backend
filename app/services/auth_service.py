from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from app.config import config

class AuthService:
    """Handles authentication-related logic such as password hashing and JWT management."""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = str(config.JWT_SECRET_KEY)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a plaintext password using bcrypt."""
        return AuthService.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies a plaintext password against a hashed password."""
        return AuthService.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """Generates a JWT access token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> dict:
        """Decodes a JWT token and returns the payload."""
        return jwt.decode(token, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
