from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.exception import NotFoundException
from app.model.product import Product
from app.schema.base import ListResponse
from app.schema.product import ProductCreate, ProductResponse, ProductUpdate


def create(*, db: Session, data: ProductCreate) -> ProductResponse:
    product: Product = Product.new(data)

    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductResponse.from_orm(product)


def read_by_id(*, db: Session, id_: int) -> ProductResponse:
    product: Product | None = db.get(Product, id_)

    _raise_if_not_exists(product)

    return ProductResponse.from_orm(product)


def read_products(
    *, db: Session, query: str | None, cursor: int, page_size: int
) -> ListResponse[ProductResponse]:
    statement = select(Product).filter(Product.id > cursor)

    if query:
        statement = statement.filter(
            or_(
                Product.name.ilike(f"%{query}%"),
                Product.name_chosung.ilike(f"%{query}%"),
            )
        )

    if page_size != -1:
        statement = statement.limit(page_size)

    products = [
        ProductResponse.from_orm(product) for product in db.scalars(statement).all()
    ]
    next_cursor = (
        products[-1].id if cursor >= 0 and products and page_size != -1 else None
    )

    return ListResponse(
        next_cursor=next_cursor,
        page_size=page_size,
        items=products,
    )


def update(*, db: Session, id_: int, data: ProductUpdate) -> ProductResponse:
    product: Product | None = db.get(Product, id_)

    _raise_if_not_exists(product)

    product.update(data)

    db.commit()
    db.refresh(product)
    return ProductResponse.from_orm(product)


def delete(*, db: Session, id_: int) -> None:
    product: Product | None = db.get(Product, id_)

    _raise_if_not_exists(product)

    db.delete(product)
    db.commit()


def _raise_if_not_exists(product: Product | None) -> None:
    if not product:
        raise NotFoundException("존재하지 않는 상품입니다.")
