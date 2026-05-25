from fastapi.testclient import TestClient

from app.main import app


def test_healthz_returns_service_status():
    client = TestClient(app)

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "service": "vos-studio-bff",
        "version": "0.1.0",
    }


def test_capabilities_redacts_sensitive_values():
    client = TestClient(app)

    response = client.get("/api/capabilities")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "vos-studio-bff"
    assert body["api"]["contract_version"] == "2026-05-24"
    assert body["auth"]["cookie_session"] is True
    assert body["auth"]["csrf_required"] is True
    assert "mcp_token" not in str(body).lower()
    assert "session_secret" not in str(body).lower()
