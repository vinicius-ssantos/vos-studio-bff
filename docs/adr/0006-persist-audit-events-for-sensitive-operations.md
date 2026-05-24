# ADR-0006 — Persist audit events for sensitive operations

Status: Accepted  
Date: 2026-05-24

## Context

VOS Studio handles client data, creative assets, provider jobs, approvals, budget constraints, and external notifications.

Operators need traceability for who requested an operation, what was approved, what was executed, and whether it succeeded.

`vos-studio-mcp` already contains domain audit concepts. The BFF also needs an audit trail for browser-side decisions and policy enforcement.

## Decision

The BFF persists audit events for sensitive browser-triggered operations.

Audit events should include:

```text
actor
role
action
entity_type
entity_id
risk_level
arguments_hash
arguments_redacted
approval_status
result
failure_reason
request_id
created_at
```

The BFF must not persist raw secrets, provider tokens, Authorization headers, cookies, or unredacted sensitive fields.

## Consequences

Operators can review UI-triggered operational history.

Security investigations can distinguish browser intent, BFF policy decisions, MCP execution, and downstream provider effects.

Audit storage can start simple but must be production-persistent before real operational use.
