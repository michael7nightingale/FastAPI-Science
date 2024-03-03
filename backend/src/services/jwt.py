from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import ValidationError

from src.core.config import get_app_settings
from src.apps.users.schemas import Token


def encode_jwt_token(user_id: str) -> str:
    settings = get_app_settings()
    token = Token(
        user_id=user_id,
        type=type,
        exp=datetime.now() + timedelta(minutes=settings.EXPIRE_MINUTES)
    )
    return jwt.encode(
        token.model_dump(),
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_jwt_token(encoded_token: str) -> Token | None:
    settings = get_app_settings()
    try:
        payload = jwt.decode(
            token=encoded_token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return Token(**payload)
    except (JWTError, ValidationError):
        return
