from enum import StrEnum

from pydantic import Field

from app.schema.base import Schema


class Category(StrEnum):
    FOOD = "FOOD"
    CLOTH = "CLOTH"
    ETC = "ETC"


class ProductSize(StrEnum):
    SMALL = "SMALL"
    LARGE = "LARGE"


class _ProductBase(Schema):
    category: Category = Field(description="카테고리")
    price: int = Field(description="가격")
    cost: int = Field(description="원가")
    name: str = Field(description="이름")
    description: str = Field(description="설명")
    barcode: str = Field(description="바코드")
    expiry_date: str = Field(description="유통기한")
    size: ProductSize = Field(description="사이즈")


class ProductCreate(_ProductBase):
    pass


class ProductUpdate(_ProductBase):
    pass


class ProductResponse(_ProductBase):
    id: int = Field(description="ID")

    class Config:
        orm_mode = True
