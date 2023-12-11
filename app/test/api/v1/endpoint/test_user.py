from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schema.user import UserCreate


def test_create_user_success(client: TestClient):
    # given
    data = {"tel": "01012345678", "password": "1234"}

    # when
    response = client.post(
        "api/v1/users",
        json=data,
    )

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["tel"] == "01012345678"
    assert response.json()["data"]["id"] is not None


def test_raise_conflict_exception_when_try_to_create_same_tel_user(
    client: TestClient, db: Session
):
    # given
    data = {"tel": "01012345678", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    response = client.post(
        "api/v1/users",
        json=data,
    )

    # then
    assert response.status_code == 409
    assert response.json()["meta"]["code"] == 409
    assert response.json()["meta"]["message"] == "'01012345678'는 이미 사용 중인 휴대폰 번호입니다."
    assert response.json()["data"] is None
