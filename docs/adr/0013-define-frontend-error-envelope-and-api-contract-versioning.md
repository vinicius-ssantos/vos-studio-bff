# ADR-0013 — Define frontend error envelope and API contract versioning

Status: Proposed  
Date: 2026-05-24

## Context

The web console needs predictable error handling for authentication failures, CSRF failures, RBAC denials, rate limits, MCP downtime, provider failures, and validation errors.

If each endpoint returns ad hoc errors, the frontend will need fragile per-endpoint handling and may accidentally display sensitive backend details.

The BFF also needs a way to evolve endpoint contracts without breaking the frontend unexpectedly.

## Decision

All `/api/*` error responses should use a stable envelope:

```json
{
  "error": {
    "code": "forbidden",
    "message": "You do not have permission to perform this action.",
    "request_id": "req_...",
    "details": {}
  }
}
```

Expected error codes should include:

```text
unauthorized
forbidden
csrf_failed
rate_limited
validation_failed
not_found
conflict
mcp_unreachable
mcp_timeout
mcp_server_error
operation_expired
operation_requires_confirmation
request_failed
```

The BFF must not include secrets, raw provider payloads, stack traces, Authorization headers, cookies, or unredacted MCP payloads in browser-facing errors.

The BFF should expose a contract version through `/api/capabilities`, for example:

```json
{
  "api": {
    "contract_version": "2026-05-24"
  }
}
```

## Consequences

The frontend can implement consistent error UX.

Backend internals remain hidden from the browser.

Breaking API changes require an explicit contract version bump or compatibility layer.
