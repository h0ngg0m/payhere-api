from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


def camelize(s: str) -> str:
    words = s.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class Schema(BaseModel):
    class Config:
        alias_generator = camelize  # camelize 함수로 별칭을 만든다.
        allow_population_by_field_name = True  # alias로 지정한 이름으로 필드를 접근할 수 있게 해준다.


T = TypeVar("T")


class ListResponse(Schema, GenericModel, Generic[T]):
    next_cursor: int | None = Field(None, description="다음 페이지 커서")
    page_size: int | None = Field(None, description="페이지당 아이템 개수, -1인 경우 모든 아이템 조회")
    items: list[T] = Field(description="아이템 목록")


class Meta(Schema):
    code: int = Field(200, description="응답 코드")
    message: str = Field("ok", description="응답 메세지")


class CommonResponse(Schema, GenericModel, Generic[T]):
    meta: Meta = Field(Meta(), description="메타 정보")
    data: T = Field(None, description="응답 데이터")
