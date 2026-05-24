# ADR-0015 — Validate runtime configuration and secret handling

Status: Proposed  
Date: 2026-05-24

## Context

The BFF will hold browser session secrets, OAuth client secrets, MCP credentials, CSRF material, CORS settings, cookie settings, and audit storage configuration.

Unsafe production configuration can silently weaken the security boundary even when application code is correct.

The implementation baseline already includes production configuration validation. VOS Studio needs equivalent validation adapted to its domain.

## Decision

The BFF must fail fast at startup when production configuration is unsafe.

Production validation should reject:

```text
missing or default session secret
missing MCP credential
non-HTTPS MCP URL
non-HTTPS frontend URL
wildcard ALLOWED_ORIGINS
COOKIE_SECURE=false
COOKIE_SAMESITE=none with insecure cookies
raw MCP passthrough enabled
unknown tools allowed by default
non-persistent audit storage for production
```

The BFF must never expose secrets through:

```text
/api/capabilities
/healthz
logs
metrics labels
error responses
audit event payloads
frontend environment variables
```

Configuration examples must use placeholders and development-only values clearly marked as unsafe for production.

## Consequences

Misconfigured production deploys fail visibly instead of operating with weak security.

Local development remains possible with explicit development settings.

Secret redaction becomes a core acceptance criterion for implementation PRs.
