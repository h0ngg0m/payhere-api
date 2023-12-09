from enum import StrEnum

from app.schema.base import Schema


class Category(StrEnum):
    FOOD = "FOOD"
    CLOTH = "CLOTH"
    ETC = "ETC"


class ProductSize(StrEnum):
    SMALL = "SMALL"
    LARGE = "LARGE"


class _ProductBase(Schema):
    category: Category
    price: int
    cost: int
    name: str
    description: str
    barcode: str
    expiry_date: str
    size: ProductSize


class ProductCreate(_ProductBase):
    pass


class ProductUpdate(_ProductBase):
    pass


class ProductResponse(_ProductBase):
    id: int

    class Config:
        orm_mode = True
