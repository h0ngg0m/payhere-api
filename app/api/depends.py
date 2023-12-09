from typing import Annotated

from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core import security
from app.core.config import settings
from app.core.db.session import SessionLocal
from app.core.exception import NotFoundException, UnauthorizedException
from app.model.user import User
from app.schema.token import TokenPayload


def get_token(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise UnauthorizedException("권한이 없습니다.")
    return authorization.split(" ")[1]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDepends = Annotated[Session, Depends(get_db)]
TokenDepends = Annotated[str, Depends(get_token)]


def get_current_user(session: SessionDepends, token: TokenDepends) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )

        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise UnauthorizedException("권한이 없습니다.")

    user = session.get(User, token_data.sub)

    if not user:
        raise NotFoundException("존재하지 않는 회원입니다.")

    if user.logout_flag:
        raise UnauthorizedException("로그아웃되었습니다. 다시 로그인 해주세요.")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
