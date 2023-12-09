from fastapi.testclient import TestClient


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
    assert response.json()["data"]["tel"] == "01012345678"
    assert response.json()["data"]["id"] is not None
