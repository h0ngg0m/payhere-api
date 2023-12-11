import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.exception import NotFoundException
from app.crud import crud_product
from app.schema.product import ProductCreate


def test_raise_unauthorized_exception_when_create_without_access_token(
    client: TestClient,
):
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
    response = client.post("api/v1/products", json=data)

    # then
    assert response.status_code == 401
    assert response.json()["meta"]["code"] == 401
    assert response.json()["meta"]["message"] == "권한이 없습니다."
    assert response.json()["data"] is None


def test_create_products_success(client: TestClient, access_token: dict):
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
    response = client.post("api/v1/products", json=data, headers=access_token)

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"

    response_data = response.json()["data"]
    assert response_data["category"] == "FOOD"
    assert response_data["price"] == 1000
    assert response_data["cost"] == 500
    assert response_data["name"] == "test"
    assert response_data["description"] == "test"
    assert response_data["barcode"] == "1234567890123"
    assert response_data["expiryDate"] == "2023-03-25 13:45:30"
    assert response_data["size"] == "SMALL"
    assert response_data["id"] is not None


def test_read_product_by_id_success(
    client: TestClient, access_token: dict, db: Session
):
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
    response = client.get(f"api/v1/products/{product.id}", headers=access_token)

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"

    response_data = response.json()["data"]
    assert response_data["category"] == "FOOD"
    assert response_data["price"] == 1000
    assert response_data["cost"] == 500
    assert response_data["name"] == "test"
    assert response_data["description"] == "test"
    assert response_data["barcode"] == "1234567890123"
    assert response_data["expiryDate"] == "2023-03-25 13:45:30"
    assert response_data["size"] == "SMALL"
    assert response_data["id"] is not None


def test_raise_if_not_exists_when_read_product_by_id(
    client: TestClient, access_token: dict, db: Session
):
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
    response = client.get(f"api/v1/products/{product.id + 1}", headers=access_token)

    # then
    assert response.status_code == 404
    assert response.json()["meta"]["code"] == 404
    assert response.json()["meta"]["message"] == "존재하지 않는 상품입니다."
    assert response.json()["data"] is None


def test_update_product_success(client: TestClient, access_token: dict, db: Session):
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
        "price": 1500,
        "cost": 700,
        "name": "beast",
        "description": "beast",
        "barcode": "101010101",
        "expiry_date": "2123-03-25 13:45:30",
        "size": "LARGE",
    }
    response = client.put(
        f"api/v1/products/{product.id}", headers=access_token, json=new_data
    )

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"

    response_data = response.json()["data"]
    assert response_data["category"] == "CLOTH"
    assert response_data["price"] == 1500
    assert response_data["cost"] == 700
    assert response_data["name"] == "beast"
    assert response_data["description"] == "beast"
    assert response_data["barcode"] == "101010101"
    assert response_data["expiryDate"] == "2123-03-25 13:45:30"
    assert response_data["size"] == "LARGE"
    assert response_data["id"] is not None


def test_raise_if_not_exists_when_update(
    client: TestClient, access_token: dict, db: Session
):
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
    response = client.put(
        f"api/v1/products/{product.id + 1}", json=data, headers=access_token
    )

    # then
    assert response.status_code == 404
    assert response.json()["meta"]["code"] == 404
    assert response.json()["meta"]["message"] == "존재하지 않는 상품입니다."
    assert response.json()["data"] is None


def test_delete_product_success(client: TestClient, access_token: dict, db: Session):
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
    response = client.delete(f"api/v1/products/{product.id}", headers=access_token)

    # then
    assert response.status_code == 204
    with pytest.raises(NotFoundException) as error_info:
        crud_product.read_by_id(db=db, id_=product.id)
    assert error_info.value.args[0] == "존재하지 않는 상품입니다."


def test_raise_if_not_exists_when_delete(
    client: TestClient, access_token: dict, db: Session
):
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
    response = client.delete(f"api/v1/products/{product.id + 1}", headers=access_token)

    # then
    assert response.status_code == 404
    assert response.json()["meta"]["code"] == 404
    assert response.json()["meta"]["message"] == "존재하지 않는 상품입니다."
    assert response.json()["data"] is None
