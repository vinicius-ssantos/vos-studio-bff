# ADR-0001 — Use a dedicated BFF for the VOS Studio internal console

Status: Accepted  
Date: 2026-05-24

## Context

`vos-studio-mcp` is the operational MCP server for VOS Studio creative workflows. It exposes MCP tools for agents and operational endpoints such as health, metrics, and webhooks.

A browser-based internal console has different requirements from an MCP client. It needs UI-friendly views, browser sessions, CSRF protection, role-based access control, and safe handling of state-changing actions.

Putting all frontend-specific behavior directly into `vos-studio-mcp` would couple the MCP server to browser UI concerns and increase the risk of exposing MCP credentials or internal operation details.

## Decision

Create `vos-studio-bff` as a dedicated Backend for Frontend for the VOS Studio internal web console.

The intended topology is:

```text
Browser / VOS Studio Console
  → vos-studio-bff
      → vos-studio-mcp
          → database, queue, storage, providers, webhooks
```

The BFF is responsible for browser-facing concerns. The MCP server remains responsible for creative workflow orchestration, persistence, provider adapters, queue integration, and MCP tool execution.

## Consequences

The frontend must call the BFF, not the MCP server directly.

The BFF may expose UI-oriented REST endpoints while internally calling MCP tools or future REST endpoints on `vos-studio-mcp`.

This adds one deployable service, but keeps browser security, UI contracts, and MCP execution boundaries explicit.
