from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(*, subject: str | Any, expires_delta: timedelta) -> str:
    to_encode = {"exp": datetime.now(timezone.utc) + expires_delta, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
