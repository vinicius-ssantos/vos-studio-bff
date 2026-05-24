# ADR-0011 — Define observability and operational health model

Status: Proposed  
Date: 2026-05-24

## Context

The BFF sits on the critical path between the browser console and `vos-studio-mcp`.

When the console fails, operators need to know whether the problem is frontend session state, BFF auth/policy, MCP availability, database/queue/storage health behind the MCP, or downstream provider behavior.

`vos-studio-mcp` already exposes health and metrics. The BFF should add its own diagnostics without leaking secrets.

## Decision

The BFF exposes safe health and capability endpoints:

```text
GET /healthz
GET /api/capabilities
```

The BFF should report:

```text
service status
BFF version
runtime environment
MCP reachability
configured auth mode, without secrets
CSRF requirement
feature flags
rate limits
```

The BFF should generate or propagate a correlation/request ID for each request and include it in logs and calls to MCP.

Sensitive values must not appear in logs, metrics labels, health payloads, or error responses.

## Consequences

Operators can distinguish BFF failure from MCP failure.

Frontend can adapt to enabled capabilities without guessing.

Observability must be implemented early because debugging auth, CSRF, and MCP proxy issues is otherwise slow.
