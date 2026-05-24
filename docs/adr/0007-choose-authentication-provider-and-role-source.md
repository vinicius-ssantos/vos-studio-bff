# ADR-0007 — Choose authentication provider and role source

Status: Proposed  
Date: 2026-05-24

## Context

The VOS Studio console needs authenticated browser users. The BFF must map those users to roles such as viewer, operator, and admin.

`vos-studio-mcp` already supports validating Bearer tokens from an external identity provider and can derive `client_id` from token claims. The BFF has a different need: browser login, session cookies, CSRF, and UI roles.

The implementation baseline from `github-unified-mcp-bff` already supports GitHub OAuth and username/team-based RBAC. VOS Studio may also use Supabase Auth because the MCP stack already expects Supabase/Postgres as system of record.

## Decision

Use the simplest provider that supports the current operating model, but keep the BFF auth boundary provider-agnostic.

Initial implementation may reuse GitHub OAuth from the existing BFF baseline for admin/operator access.

The BFF must define a role source abstraction so future Supabase Auth, Google Workspace, or another IdP can replace GitHub OAuth without rewriting endpoint policy.

The BFF role model remains:

```text
viewer
operator
admin
```

Role assignment can start with environment-configured allowlists, but production should move toward a persistent role source.

## Open questions

- Should VOS Studio operators authenticate with GitHub, Supabase Auth, or Google Workspace first?
- Should client-facing users exist in this console, or should the first version be internal-only?
- Should `client_id` access be derived from IdP metadata, a BFF database, or MCP ownership checks?

## Consequences

GitHub OAuth is fastest if only internal operators use the console.

Supabase Auth may be better if the console later includes client-facing access.

The BFF must not hard-code GitHub-specific assumptions into business endpoints.
