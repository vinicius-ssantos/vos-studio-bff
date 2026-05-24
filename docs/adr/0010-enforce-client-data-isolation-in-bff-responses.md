# ADR-0010 — Enforce client data isolation in BFF responses

Status: Proposed  
Date: 2026-05-24

## Context

VOS Studio stores client data, brand kits, creative briefs, prompt packs, generated assets, provider job metadata, and performance records.

The BFF shapes UI responses and therefore becomes a second line of defense against accidental cross-client data exposure.

`vos-studio-mcp` must remain the source of truth for domain ownership checks, but the BFF must also avoid broad or unfiltered responses.

## Decision

Every BFF endpoint that returns client-scoped data must apply explicit client isolation rules.

The BFF should derive the allowed client scope from the authenticated session, role source, or MCP response context.

Default behavior:

```text
viewer/operator — only assigned client scopes
admin           — may access all clients, but UI should still require explicit selection/filtering
```

BFF responses must be compact DTOs and should not include raw provider payloads, secrets, full prompt internals, or unrelated client records.

The BFF should prefer endpoints that require explicit `client_id` or `sprint_id` rather than broad global listings.

## Consequences

The BFF does not replace MCP-side ownership checks.

The BFF reduces blast radius if a UI route or component is misconfigured.

Admin access remains powerful but should be intentional and auditable.
