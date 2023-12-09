from typing import Dict

from fastapi.testclient import TestClient


def get_access_token(client: TestClient) -> Dict[str, str]:
    data = {"tel": "01099998888", "password": "1234"}
    rr = client.post(
        "api/v1/users",
        json=data,
    )
    response = client.post(
        "api/v1/auth/login", data={"username": "01099998888", "password": "1234"}
    )
    access_token = response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
