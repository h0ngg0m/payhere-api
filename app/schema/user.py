from pydantic import Field, validator

from app.core.exception import BadRequestException
from app.schema.base import Schema


class UserCreate(Schema):
    tel: str = Field(description="휴대폰 번호 (휴대폰 번호는 숫자로 된 11자리여야 합니다)")
    password: str = Field(description="비밀번호")

    @validator("tel")
    def validate_tel(cls, tel: str) -> str:
        if len(tel) != 11 or not tel.isdigit():
            raise BadRequestException("휴대폰 번호는 숫자로 된 11자리여야 합니다.")
        return tel


class UserResponse(Schema):
    id: int = Field(description="ID")
    tel: str = Field(description="휴대폰 번호")

    class Config:
        orm_mode = True


class UserLogin(Schema):
    tel: str = Field(description="휴대폰 번호 (휴대폰 번호는 숫자로 된 11자리여야 합니다)")
    password: str = Field(description="비밀번호")
