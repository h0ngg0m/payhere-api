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

    if not product:
        raise NotFoundException("존재하지 않는 상품입니다.")

    return ProductResponse.from_orm(product)


def read_products(
    *, db: Session, query: str | None, cursor: int | None, page_size: int | None
) -> ListResponse[ProductResponse]:
    statement = select(Product).order_by(Product.id.desc())

    if query:
        statement = statement.filter(
            or_(
                Product.name.ilike(f"%{query}%"),
                Product.name_chosung.ilike(f"%{query}%"),
            )
        )

    if cursor:
        statement = statement.filter(Product.id <= cursor)

    if page_size:
        statement = statement.limit(page_size)

    products = [
        ProductResponse.from_orm(product) for product in db.scalars(statement).all()
    ]

    return ListResponse(
        next_cursor=products[-1].id - 1 if cursor and products else None,
        page_size=page_size if page_size else None,
        items=products,
    )


def update(*, db: Session, id_: int, data: ProductUpdate) -> ProductResponse:
    product: Product | None = db.get(Product, id_)

    if not product:
        raise NotFoundException("존재하지 않는 상품입니다.")

    product.update(data)

    db.flush()
    db.commit()
    db.refresh(product)

    return ProductResponse.from_orm(product)


def delete(*, db: Session, id_: int) -> None:
    product: Product | None = db.get(Product, id_)

    if not product:
        raise NotFoundException("존재하지 않는 상품입니다.")

    db.delete(product)
    db.commit()
