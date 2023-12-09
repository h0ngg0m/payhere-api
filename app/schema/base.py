from datetime import datetime, timezone
from typing import Generic, TypeVar

from orjson import loads
from pydantic import BaseModel


def camelize(s: str) -> str:
    words = s.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class Schema(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        json_loads = loads
        json_encoders = {
            datetime: lambda v: v.astimezone(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
        }


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
