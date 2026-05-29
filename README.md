# VOS Studio BFF

Backend for Frontend for the VOS Studio internal web console.

This service sits between the browser-based console and `vos-studio-mcp`.
It exists to keep MCP credentials and provider-facing operations server-side while giving operators a safe UI-oriented API.

```text
Browser / VOS Studio Console
  → VOS Studio BFF
      → vos-studio-mcp
          → Postgres, Redis/Celery, storage, providers, webhooks
```

## Initial scope

- Cookie-based authenticated browser session.
- CSRF protection for state-changing requests.
- RBAC for viewer, operator, and admin roles.
- Server-side MCP token handling.
- VOS-specific tool policy.
- Controlled preview/confirmation flow for paid or external actions.
- UI-friendly `/api/vos/*` endpoints.
- Audit log for sensitive operations.

## Architecture decisions

Architecture Decision Records live in [`docs/adr`](docs/adr/README.md).

## Container runtime

The service image runs the FastAPI app with Uvicorn on port `8000`:

```bash
docker build -t vos-studio-bff:test .
docker run --rm -p 8030:8000 \
  -e BFF_ENV=development \
  -e FRONTEND_URL=http://localhost:5174 \
  -e ALLOWED_ORIGINS=http://localhost:5174 \
  -e MCP_URL=http://vos-studio-mcp:8000 \
  -e COOKIE_SECURE=false \
  vos-studio-bff:test
```

Health check:

```bash
curl -fsS http://localhost:8030/healthz
```
