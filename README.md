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
