from typing import Dict

from fastapi.testclient import TestClient


def get_access_token(client: TestClient) -> Dict[str, str]:
    data = {"tel": "01099998888", "password": "1234"}
    client.post(
        "api/v1/users",
        json=data,
    )
    response = client.post(
        "api/v1/auth/login", json={"tel": "01099998888", "password": "1234"}
    )
    access_token = response.json()["data"]["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
