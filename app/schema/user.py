from pydantic import validator

from app.core.exception import BadRequestException
from app.schema.base import Schema


class UserCreate(Schema):
    tel: str
    password: str

    @validator("tel")
    def validate_tel(cls, tel: str) -> str:
        if len(tel) != 11 or not tel.isdigit():
            raise BadRequestException("휴대폰 번호는 숫자로 된 11자리여야 합니다.")
        return tel


class UserResponse(Schema):
    id: int
    tel: str

    class Config:
        orm_mode = True
