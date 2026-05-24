# ADR-0002 — Keep browser sessions and MCP credentials separated

Status: Accepted  
Date: 2026-05-24

## Context

The VOS Studio console needs authenticated browser access. The MCP server also requires Bearer tokens for protected tool execution.

Exposing MCP tokens, provider credentials, storage credentials, Supabase service secrets, or long-lived internal tokens to the browser would create a severe security risk.

The BFF pattern allows the browser to authenticate with a short-lived session while the BFF keeps internal credentials server-side.

## Decision

The browser authenticates to `vos-studio-bff` using a cookie-based session.

The BFF authenticates to `vos-studio-mcp` using server-side credentials. These credentials must never be returned to the browser, written into frontend configuration, or logged.

Session cookies should be `HttpOnly`. State-changing requests must use CSRF protection.

Production configuration must use explicit allowed origins and must reject wildcard CORS.

## Consequences

The frontend can operate without access to MCP credentials.

The BFF becomes the enforcement point for browser session validation, CSRF, CORS, and user role checks.

Any future login provider can be added at the BFF layer without changing MCP tool implementation.
