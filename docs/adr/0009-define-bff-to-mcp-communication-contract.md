# ADR-0009 — Define BFF-to-MCP communication contract

Status: Proposed  
Date: 2026-05-24

## Context

The BFF needs to call `vos-studio-mcp` to read and execute creative workflow operations.

There are two possible integration styles:

1. BFF calls MCP JSON-RPC tools through `/mcp`.
2. BFF calls future REST endpoints exposed by `vos-studio-mcp`.

Direct database access from the BFF would bypass domain services, audit rules, client ownership checks, and provider orchestration.

## Decision

The BFF must not access the VOS production database directly for domain operations.

The initial BFF-to-MCP integration should use server-side MCP calls for existing capabilities.

The BFF may later use REST endpoints on `vos-studio-mcp` when a workflow benefits from a stable HTTP API contract.

Every BFF call to MCP must include:

```text
request_id / correlation_id
actor identity
role or policy context when relevant
server-side MCP authorization
safe timeout
structured error mapping
```

The BFF should normalize MCP responses into UI DTOs instead of passing raw MCP payloads to the browser.

## Consequences

Domain rules remain centralized in `vos-studio-mcp`.

The BFF can evolve UI contracts without exposing MCP protocol details.

If `/api/vos/*` endpoints become heavily used, corresponding stable REST endpoints may be added to the MCP server later.
