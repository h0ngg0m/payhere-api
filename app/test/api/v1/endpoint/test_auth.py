from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schema.user import UserCreate


def test_login_success(client: TestClient, db: Session):
    # given
    data = {"tel": "01012340987", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    response = client.post(
        "api/v1/auth/login", data={"username": "01012340987", "password": "1234"}
    )

    # then
    assert response.status_code == 200
    assert response.json()["data"]["access_token"] is not None


def test_logout_success(client: TestClient, access_token: dict):
    # given, when
    response = client.delete("api/v1/auth/logout", headers=access_token)

    # then
    assert response.status_code == 204
