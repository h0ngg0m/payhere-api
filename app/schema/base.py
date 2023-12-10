from typing import Generic, TypeVar

from pydantic import BaseModel


def camelize(s: str) -> str:
    words = s.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class Schema(BaseModel):
    class Config:
        alias_generator = camelize  # camelize 함수로 별칭을 만든다.
        allow_population_by_field_name = True  # alias로 지정한 이름으로 필드를 접근할 수 있게 해준다.


T = TypeVar("T")


class ListResponse(Schema, Generic[T]):
    next_cursor: int | None
    page_size: int | None
    items: list[T]


class Meta(Schema):
    code: int = 200
    message: str = "oK"


class CommonResponse(Schema, Generic[T]):
    meta: Meta = Meta()
    data: T = None
