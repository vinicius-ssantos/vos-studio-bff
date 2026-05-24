# ADR-0012 — Reuse the GitHub Unified MCP BFF as implementation baseline

Status: Proposed  
Date: 2026-05-24

## Context

The existing `-github-unified-mcp-bff` repository already implements many browser-facing safety mechanisms needed by `vos-studio-bff`:

```text
FastAPI application structure
CORS configuration
GitHub OAuth flow
HttpOnly session cookie
CSRF token
RBAC
rate limiting
MCP proxying
structured tool calls
local tool policy
audit log
controlled operation preview/confirmation
production config validation
```

Creating all of these from scratch would add risk and delay.

However, the existing BFF is coupled to GitHub MCP tools, GitHub-specific policy names, and GitHub operations.

## Decision

Use `-github-unified-mcp-bff` as the implementation baseline, not as a runtime dependency.

Port the reusable infrastructure into `vos-studio-bff`, then rename and adapt domain concepts to VOS Studio.

The first implementation PRs should avoid broad copy-paste of unrelated GitHub behavior. They should move in small slices:

```text
1. project scaffold and config validation
2. health and capabilities
3. auth/session/CSRF
4. MCP client/proxy
5. VOS tool policy
6. audit storage
7. controlled operations
8. /api/vos/* endpoint facades
```

## Consequences

The BFF starts from proven security patterns.

The VOS repo gets its own identity, policy, docs, and release cadence.

GitHub-specific tools must be removed or replaced before production use.
