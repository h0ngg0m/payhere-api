from typing import Optional

from app.schema.base import Schema


class Token(Schema):
    access_token: str
    token_type: str


class TokenPayload(Schema):
    sub: int | None = None
