import pytest
from sqlalchemy.orm import Session

from app.core.exception import NotFoundException
from app.crud import crud_product
from app.schema.product import ProductCreate, ProductUpdate


def test_create_success(db: Session):
    # given
    data = {
        "category": "FOOD",
        "price": 1000,
        "cost": 500,
        "name": "test",
        "description": "test",
        "barcode": "1234567890123",
        "expiry_date": "2023-03-25 13:45:30",
        "size": "SMALL",
    }

    # when
    product = crud_product.create(db=db, data=ProductCreate(**data))

    # then
    assert product is not None
    assert product.category == "FOOD"
    assert product.price == 1000
    assert product.cost == 500
    assert product.name == "test"
    assert product.description == "test"
    assert product.barcode == "1234567890123"
    assert product.expiry_date == "2023-03-25 13:45:30"
    assert product.size == "SMALL"
    assert product.id is not None


def test_read_by_id(db: Session):
    # given
    data = {
        "category": "FOOD",
        "price": 1000,
        "cost": 500,
        "name": "test",
        "description": "test",
        "barcode": "1234567890123",
        "expiry_date": "2023-03-25 13:45:30",
        "size": "SMALL",
    }
    product = crud_product.create(db=db, data=ProductCreate(**data))

    # when
    product = crud_product.read_by_id(db=db, id_=product.id)

    # then
    assert product is not None
    assert product.category == "FOOD"
    assert product.price == 1000
    assert product.cost == 500
    assert product.name == "test"
    assert product.description == "test"
    assert product.barcode == "1234567890123"
    assert product.expiry_date == "2023-03-25 13:45:30"
    assert product.size == "SMALL"
    assert product.id is not None


def test_raise_if_not_exists_when_read_by_id(db: Session):
    # given
    data = {
        "category": "FOOD",
        "price": 1000,
        "cost": 500,
        "name": "test",
        "description": "test",
        "barcode": "1234567890123",
        "expiry_date": "2023-03-25 13:45:30",
        "size": "SMALL",
    }
    product = crud_product.create(db=db, data=ProductCreate(**data))

    # when, then
    with pytest.raises(NotFoundException) as error_info:
        crud_product.read_by_id(db=db, id_=product.id + 1)
    assert error_info.value.args[0] == "존재하지 않는 상품입니다."


def test_update_success(db: Session):
    # given
    data = {
        "category": "FOOD",
        "price": 1000,
        "cost": 500,
        "name": "test",
        "description": "test",
        "barcode": "1234567890123",
        "expiry_date": "2023-03-25 13:45:30",
        "size": "SMALL",
    }
    product = crud_product.create(db=db, data=ProductCreate(**data))

    # when
    new_data = {
        "category": "CLOTH",
        "price": 1200,
        "cost": 700,
        "name": "test2",
        "description": "test2",
        "barcode": "1234",
        "expiry_date": "2123-03-25 13:45:30",
        "size": "LARGE",
    }
    product = crud_product.update(db=db, id_=product.id, data=ProductUpdate(**new_data))

    # then
    assert product is not None
    assert product.category == "CLOTH"
    assert product.price == 1200
    assert product.cost == 700
    assert product.name == "test2"
    assert product.description == "test2"
    assert product.barcode == "1234"
    assert product.expiry_date == "2123-03-25 13:45:30"
    assert product.size == "LARGE"
    assert product.id is not None


def test_raise_if_not_exists_when_update(db: Session):
    # given
    data = {
        "category": "FOOD",
        "price": 1000,
        "cost": 500,
        "name": "test",
        "description": "test",
        "barcode": "1234567890123",
        "expiry_date": "2023-03-25 13:45:30",
        "size": "SMALL",
    }
    product = crud_product.create(db=db, data=ProductCreate(**data))
    new_data = {
        "category": "CLOTH",
        "price": 1200,
        "cost": 700,
        "name": "test2",
        "description": "test2",
        "barcode": "1234",
        "expiry_date": "2123-03-25 13:45:30",
        "size": "LARGE",
    }

    # when, then
    with pytest.raises(NotFoundException) as error_info:
        crud_product.update(db=db, id_=product.id + 1, data=ProductUpdate(**new_data))
    assert error_info.value.args[0] == "존재하지 않는 상품입니다."


def test_delete_success(db: Session):
    # given
    data = {
        "category": "FOOD",
        "price": 1000,
        "cost": 500,
        "name": "test",
        "description": "test",
        "barcode": "1234567890123",
        "expiry_date": "2023-03-25 13:45:30",
        "size": "SMALL",
    }
    product = crud_product.create(db=db, data=ProductCreate(**data))

    # when
    crud_product.delete(db=db, id_=product.id)

    # then
    with pytest.raises(NotFoundException) as error_info:
        crud_product.read_by_id(db=db, id_=product.id)
    assert error_info.value.args[0] == "존재하지 않는 상품입니다."


def test_raise_if_not_exists_when_delete(db: Session):
    # when, then
    with pytest.raises(NotFoundException) as error_info:
        crud_product.delete(db=db, id_=9999)
    assert error_info.value.args[0] == "존재하지 않는 상품입니다."
