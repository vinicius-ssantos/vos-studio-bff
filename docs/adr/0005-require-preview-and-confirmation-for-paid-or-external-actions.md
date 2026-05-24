# ADR-0005 — Require preview and confirmation for paid or external actions

Status: Accepted  
Date: 2026-05-24

## Context

VOS Studio workflows can include actions that spend provider credits, trigger API billing, retry expensive jobs, publish or deliver client-facing output, send webhooks, or modify external systems.

The MCP architecture already treats human approval as a core safety boundary. The web console must preserve that boundary rather than bypass it.

## Decision

The BFF uses a controlled operation flow for high-risk actions:

```text
1. preview
2. explicit confirmation
3. server-side execution
4. audit result
```

Preview responses must redact sensitive arguments and include enough information for a human to understand the action, expected cost, target entity, provider, and risk level.

High-risk confirmations require an explicit confirmation phrase or equivalent UI affordance. The browser must not execute paid or external actions in a single blind request.

## Consequences

The UI can safely show operators what will happen before execution.

The BFF can prevent duplicate confirmations, stale previews, tampered arguments, and privilege escalation.

The audit log can record the full lifecycle from preview to result.
