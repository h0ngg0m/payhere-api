from pydantic import Field

from app.schema.base import Schema


class Token(Schema):
    access_token: str = Field(description="액세스 토큰")
    token_type: str = Field(description="토큰 종류")


class TokenPayload(Schema):
    sub: int | None = Field(None, description="토큰 내용")
