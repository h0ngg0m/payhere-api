from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_204_NO_CONTENT

from app.api.depends import SessionDepends, CurrentUser
from app.core import security
from app.core.config import settings
from app.core.exception import UnauthorizedException
from app.crud import crud_user
from app.schema.base import CommonResponse
from app.schema.token import Token

router = APIRouter()


@router.get("")
def read_users():
    return settings


@router.post("/login", response_model=CommonResponse[Token])
def login(
    db: SessionDepends,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = crud_user.authenticate(
        db=db, tel=form_data.username, password=form_data.password
    )
    if not user:
        raise UnauthorizedException("잘못된 휴대폰 번호 또는 비밀번호입니다.")

    return CommonResponse(
        data={
            "access_token": security.create_access_token(
                subject=user.id,
                expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
            ),
            "token_type": "bearer",
        }
    )


@router.delete("/logout", status_code=HTTP_204_NO_CONTENT)
def logout(db: SessionDepends, current_user: CurrentUser):
    crud_user.logout(db=db, user=current_user)