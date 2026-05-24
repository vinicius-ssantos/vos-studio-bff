# ADR-0003 — Expose UI-oriented REST endpoints instead of direct browser MCP calls

Status: Accepted  
Date: 2026-05-24

## Context

MCP is optimized for agents and tool calls. A browser UI needs stable, view-oriented contracts: lists, filters, summaries, dashboards, detail pages, and form submissions.

Calling MCP JSON-RPC directly from the browser would expose protocol details to the UI and make it harder to enforce safe UX patterns such as previews, confirmation, pagination, and redaction.

## Decision

The BFF exposes UI-oriented REST endpoints under `/api/vos/*`.

Initial endpoint families should include:

```text
/api/vos/clients
/api/vos/brand-kits
/api/vos/sprints
/api/vos/sprints/{id}/assets
/api/vos/video-jobs
/api/vos/approvals
/api/vos/audit
/api/vos/health
```

The BFF may also expose a structured internal MCP call endpoint for controlled use, but the primary frontend contract should be `/api/vos/*`.

## Consequences

The UI can evolve independently from MCP protocol details.

The BFF can shape compact DTOs for screens and avoid returning full internal objects or sensitive payloads.

MCP tools remain available for agents and backend orchestration.
