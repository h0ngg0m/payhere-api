from sqlalchemy.orm import Mapped

from app.core.db.orm import Base, mapped_int_pk
from app.core.util import get_chosung
from app.schema.product import Category, ProductCreate, ProductSize, ProductUpdate


class Product(Base):
    __tablename__ = "product"

    id: Mapped[mapped_int_pk]
    category: Mapped[Category]
    price: Mapped[int]
    cost: Mapped[int]
    name: Mapped[str]
    name_chosung: Mapped[str]
    description: Mapped[str]
    barcode: Mapped[str]
    expiry_date: Mapped[str]
    size: Mapped[ProductSize]

    @staticmethod
    def new(data: ProductCreate) -> "Product":
        return Product(
            **data.dict(exclude={"id", "name_chosung"}),
            name_chosung=get_chosung(data.name)
        )

    def update(self, data: ProductUpdate) -> "Product":
        for key, value in data.dict(exclude={"id", "name_chosung"}).items():
            setattr(self, key, value)
        self.name_chosung = get_chosung(data.name)
        return self
