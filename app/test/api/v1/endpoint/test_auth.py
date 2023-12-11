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
        "api/v1/auth/login", json={"tel": "01012340987", "password": "1234"}
    )

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["accessToken"] is not None


def test_raise_unauthorized_exception_when_try_to_login_with_wrong_tel(
    client: TestClient, db: Session
):
    # given
    data = {"tel": "01012340987", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    response = client.post(
        "api/v1/auth/login", json={"tel": "123456789012", "password": "1234"}
    )

    # then
    assert response.status_code == 401
    assert response.json()["meta"]["code"] == 401
    assert response.json()["meta"]["message"] == "잘못된 휴대폰 번호 또는 비밀번호입니다."
    assert response.json()["data"] is None


def test_raise_unauthorized_exception_when_try_to_login_with_wrong_password(
    client: TestClient, db: Session
):
    # given
    data = {"tel": "01012340987", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    response = client.post(
        "api/v1/auth/login", json={"tel": "01012340987", "password": "4321"}
    )

    # then
    assert response.status_code == 401
    assert response.json()["meta"]["code"] == 401
    assert response.json()["meta"]["message"] == "잘못된 휴대폰 번호 또는 비밀번호입니다."
    assert response.json()["data"] is None


def test_logout_success(client: TestClient, access_token: dict):
    # given, when
    response = client.delete("api/v1/auth/logout", headers=access_token)

    # then
    assert response.status_code == 204
