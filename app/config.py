from functools import lru_cache
from urllib.parse import urlparse

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bff_env: str = "development"
    frontend_url: str = "http://localhost:5173"
    allowed_origins: str = "http://localhost:5173"
    mcp_url: str = "http://localhost:8001"
    mcp_token: str = ""
    session_secret: str = "change-me-in-production"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    rate_limit_per_user_max: int = 60
    rate_limit_per_user_window: int = 60
    allow_raw_mcp_passthrough: bool = False
    block_unknown_tools: bool = True
    audit_backend: str = "memory"
    audit_db_path: str = ""


_ALLOWED_SAMESITE = {"lax", "none", "strict"}


def is_production(settings: Settings) -> bool:
    return settings.bff_env.lower() == "production"


def _is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def parsed_allowed_origins(settings: Settings) -> list[str]:
    return [origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()]


def validate_settings(settings: Settings) -> None:
    cookie_samesite = settings.cookie_samesite.lower()
    if cookie_samesite not in _ALLOWED_SAMESITE:
        raise RuntimeError("COOKIE_SAMESITE must be one of: lax, none, strict")
    if cookie_samesite == "none" and not settings.cookie_secure:
        raise RuntimeError("COOKIE_SECURE must be true when COOKIE_SAMESITE=none")
    if not _is_http_url(settings.frontend_url):
        raise RuntimeError("FRONTEND_URL must be an http(s) URL")
    if not _is_http_url(settings.mcp_url):
        raise RuntimeError("MCP_URL must be an http(s) URL")

    if not is_production(settings):
        return

    errors: list[str] = []
    origins = parsed_allowed_origins(settings)

    if settings.session_secret in {"", "change-me-in-production"}:
        errors.append("SESSION_SECRET must be set to a strong non-default value in production")
    if not settings.mcp_token:
        errors.append("MCP_TOKEN must be configured in production")
    if not _is_https_url(settings.mcp_url):
        errors.append("MCP_URL must use https:// in production")
    if not _is_https_url(settings.frontend_url):
        errors.append("FRONTEND_URL must use https:// in production")
    if not origins:
        errors.append("ALLOWED_ORIGINS must contain at least one explicit origin in production")
    if "*" in origins:
        errors.append("ALLOWED_ORIGINS must not contain '*' in production")
    if not settings.cookie_secure:
        errors.append("COOKIE_SECURE must be true in production")
    if settings.allow_raw_mcp_passthrough:
        errors.append("ALLOW_RAW_MCP_PASSTHROUGH must be false in production")
    if not settings.block_unknown_tools:
        errors.append("BLOCK_UNKNOWN_TOOLS must be true in production")
    if settings.audit_backend.lower() == "memory":
        errors.append("AUDIT_BACKEND must be persistent in production")

    if errors:
        raise RuntimeError("Unsafe production configuration: " + "; ".join(errors))


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    validate_settings(settings)
    return settings
