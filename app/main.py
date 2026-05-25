from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import Settings, get_settings, parsed_allowed_origins


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="VOS Studio BFF", version=__version__)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=parsed_allowed_origins(settings),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthz")
    async def healthz() -> dict[str, str | bool]:
        return {"ok": True, "service": "vos-studio-bff", "version": __version__}

    @app.get("/api/capabilities")
    async def capabilities() -> dict:
        settings: Settings = get_settings()
        return {
            "service": "vos-studio-bff",
            "version": __version__,
            "environment": settings.bff_env,
            "api": {"contract_version": "2026-05-24"},
            "auth": {
                "cookie_session": True,
                "csrf_required": True,
                "cookie_samesite": settings.cookie_samesite.lower(),
                "cookie_secure": settings.cookie_secure,
            },
            "mcp": {
                "configured": bool(settings.mcp_url),
                "auth_mode": "server_side_bearer" if settings.mcp_token else "none",
                "raw_passthrough_enabled": settings.allow_raw_mcp_passthrough,
            },
            "features": {
                "audit": settings.audit_backend != "none",
                "tool_policy": True,
                "unknown_tools_blocked": settings.block_unknown_tools,
                "operation_preview": False,
                "operation_confirmation": False,
                "operation_execution": False,
            },
            "limits": {
                "rate_limit_per_user_max": settings.rate_limit_per_user_max,
                "rate_limit_per_user_window": settings.rate_limit_per_user_window,
            },
        }

    return app


app = create_app()
