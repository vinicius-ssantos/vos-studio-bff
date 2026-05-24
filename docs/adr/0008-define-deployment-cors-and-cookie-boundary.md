# ADR-0008 — Define deployment, CORS, and cookie boundary

Status: Proposed  
Date: 2026-05-24

## Context

The VOS Studio web console and BFF may be deployed on the same domain, sibling subdomains, or separate platforms.

Browser authentication relies on cookies and CSRF protection, so the deployment topology directly affects `SameSite`, `Secure`, CORS, and callback URL configuration.

Using wildcard CORS or insecure cookies in production would weaken the BFF boundary.

## Decision

Prefer a same-site deployment for production:

```text
https://studio.vosstudio.com        → frontend
https://studio.vosstudio.com/api/*  → BFF, reverse-proxied
```

If frontend and BFF must be on different origins, production must use:

```text
COOKIE_SECURE=true
COOKIE_SAMESITE=none
ALLOWED_ORIGINS=<explicit frontend origin>
```

The BFF must reject `ALLOWED_ORIGINS=*` in production.

The BFF must expose a `/api/capabilities` endpoint so the frontend can discover auth mode, CSRF requirement, environment, feature flags, and limits.

## Open questions

- Will the first deployment use Render, Railway, Vercel, or a single reverse proxy?
- Should the frontend live under the same host as the BFF from day one?
- Should the BFF provide static frontend hosting or remain API-only?

## Consequences

Same-site deployment simplifies cookies and CORS.

Cross-site deployment remains supported but requires stricter cookie and origin settings.

Deployment validation must fail fast when production settings are unsafe.
