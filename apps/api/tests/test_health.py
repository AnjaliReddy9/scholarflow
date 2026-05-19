from fastapi.testclient import TestClient

from scholarflow_api.app import create_app


def test_health_returns_typed_response() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == "0.1.0"
