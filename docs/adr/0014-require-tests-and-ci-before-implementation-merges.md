# ADR-0014 — Require tests and CI before implementation merges

Status: Proposed  
Date: 2026-05-24

## Context

The BFF will enforce authentication, sessions, CSRF, RBAC, rate limits, tool policy, audit, and controlled operation confirmation.

Regressions in these areas can expose data, bypass approvals, or break the operator console.

The implementation baseline has existing tests, but VOS-specific behavior must be validated independently.

## Decision

Implementation PRs must include tests for the security and contract behavior they introduce.

Minimum test categories:

```text
config validation
CORS and cookie settings
auth/session parsing
CSRF enforcement
RBAC role mapping
VOS tool policy
unknown tool blocking
rate limiting
MCP error mapping
controlled operation preview/confirm
audit redaction
/api/capabilities contract
```

The repository should use CI before merging implementation code.

Initial CI should run:

```text
ruff check .
pytest
```

Docker build validation should be added before production deployment.

## Consequences

Documentation-only ADR PRs may merge without runtime tests.

Implementation PRs must not rely only on manual browser testing.

Security regressions become easier to catch before deploy.
