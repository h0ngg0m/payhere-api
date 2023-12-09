import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.exception import NotFoundException
from app.crud import crud_product
from app.schema.product import ProductCreate


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
    assert response.json()["data"]["category"] == "FOOD"
    assert response.json()["data"]["price"] == 1000
    assert response.json()["data"]["cost"] == 500
    assert response.json()["data"]["name"] == "test"
    assert response.json()["data"]["description"] == "test"
    assert response.json()["data"]["barcode"] == "1234567890123"
    assert response.json()["data"]["expiryDate"] == "2023-03-25 13:45:30"
    assert response.json()["data"]["size"] == "SMALL"
    assert response.json()["data"]["id"] is not None


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
    assert response.json()["data"]["category"] == "FOOD"
    assert response.json()["data"]["price"] == 1000
    assert response.json()["data"]["cost"] == 500
    assert response.json()["data"]["name"] == "test"
    assert response.json()["data"]["description"] == "test"
    assert response.json()["data"]["barcode"] == "1234567890123"
    assert response.json()["data"]["expiryDate"] == "2023-03-25 13:45:30"
    assert response.json()["data"]["size"] == "SMALL"
    assert response.json()["data"]["id"] is not None


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
    assert response.json()["data"]["category"] == "CLOTH"
    assert response.json()["data"]["price"] == 1500
    assert response.json()["data"]["cost"] == 700
    assert response.json()["data"]["name"] == "beast"
    assert response.json()["data"]["description"] == "beast"
    assert response.json()["data"]["barcode"] == "101010101"
    assert response.json()["data"]["expiryDate"] == "2123-03-25 13:45:30"
    assert response.json()["data"]["size"] == "LARGE"
    assert response.json()["data"]["id"] is not None


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
