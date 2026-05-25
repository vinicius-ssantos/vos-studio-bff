import pytest

from app.config import Settings, parsed_allowed_origins, validate_settings


def test_parsed_allowed_origins_trims_empty_entries():
    settings = Settings(allowed_origins=" http://localhost:5173, ,https://studio.example.com ")

    assert parsed_allowed_origins(settings) == [
        "http://localhost:5173",
        "https://studio.example.com",
    ]


def test_rejects_insecure_cross_site_cookie_settings():
    settings = Settings(cookie_samesite="none", cookie_secure=False)

    with pytest.raises(RuntimeError, match="COOKIE_SECURE"):
        validate_settings(settings)


def test_production_requires_safe_settings():
    settings = Settings(bff_env="production")

    with pytest.raises(RuntimeError) as exc_info:
        validate_settings(settings)

    message = str(exc_info.value)
    assert "SESSION_SECRET" in message
    assert "MCP_TOKEN" in message
    assert "MCP_URL" in message
    assert "FRONTEND_URL" in message
    assert "COOKIE_SECURE" in message
    assert "AUDIT_BACKEND" in message


def test_accepts_safe_production_settings():
    settings = Settings(
        bff_env="production",
        frontend_url="https://studio.example.com",
        allowed_origins="https://studio.example.com",
        mcp_url="https://mcp.example.com",
        mcp_token="server-side-token",
        session_secret="strong-session-secret",
        cookie_secure=True,
        cookie_samesite="lax",
        block_unknown_tools=True,
        audit_backend="sqlite",
        audit_db_path="/var/data/audit.db",
    )

    validate_settings(settings)
