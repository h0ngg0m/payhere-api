from fastapi import APIRouter, Query
from starlette.status import HTTP_204_NO_CONTENT

from app.api.depends import SessionDepends, CurrentUser
from app.crud import crud_product
from app.schema.base import CommonResponse, ListResponse
from app.schema.product import ProductResponse, ProductCreate, ProductUpdate

router = APIRouter()


@router.post("", response_model=CommonResponse[ProductResponse])
def create_product(db: SessionDepends, data: ProductCreate, current_user: CurrentUser):
    return CommonResponse(data=crud_product.create(db=db, data=data))


@router.get("/{id_}", response_model=CommonResponse[ProductResponse])
def read_product_by_id(db: SessionDepends, id_: int, current_user: CurrentUser):
    return CommonResponse(data=crud_product.read_by_id(db=db, id_=id_))


@router.get("", response_model=CommonResponse[ListResponse[ProductResponse]])
def read_products(
    db: SessionDepends,
    current_user: CurrentUser,
    query: str | None = Query(None),
    cursor: int | None = Query(None),
    page_size: int | None = Query(default=10, alias="pageSize"),
):
    return CommonResponse(
        data=crud_product.read_products(
            db=db, query=query, cursor=cursor, page_size=page_size
        )
    )


@router.put("/{id_}", response_model=CommonResponse[ProductResponse])
def update_product(
    db: SessionDepends, id_: int, data: ProductUpdate, current_user: CurrentUser
):
    return CommonResponse(data=crud_product.update(db=db, id_=id_, data=data))


@router.delete("/{id_}", status_code=HTTP_204_NO_CONTENT)
def delete_product(db: SessionDepends, id_: int, current_user: CurrentUser):
    crud_product.delete(db=db, id_=id_)
