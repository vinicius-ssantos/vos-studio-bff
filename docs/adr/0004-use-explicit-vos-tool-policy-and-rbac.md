# ADR-0004 — Use explicit VOS tool policy and RBAC

Status: Accepted  
Date: 2026-05-24

## Context

VOS Studio operations have different risk levels. Reading sprint status is low risk. Creating a sprint or registering an asset is operationally meaningful. Running a paid generation, retrying provider work, closing a sprint, or approving delivery can have external or financial effects.

The BFF must not forward arbitrary tool calls from the browser without local policy checks.

## Decision

The BFF maintains an explicit VOS tool policy and role mapping.

Initial roles:

```text
viewer   — read-only operational visibility
operator — create and update normal workflow objects
admin    — paid, external, destructive, or finalizing actions
```

Unknown tools are blocked by default.

Initial risk categories:

```text
low:
  status
  get_sprint_status
  list_sprint_assets
  get_video_job_status
  list_video_jobs
  search_library

medium:
  create_client
  save_brand_kit
  create_creative_sprint
  prepare_dashboard_pack
  register_manual_asset
  record_asset_performance
  record_performance_metrics
  promote_to_library

high:
  request_api_video
  close_sprint
  conclude_variant_test
  approve_paid_generation
  retry_provider_job
```

## Consequences

Every browser-triggered operation must pass through BFF policy before reaching the MCP server.

Adding a new MCP tool that should be callable from the UI requires updating the BFF policy explicitly.

This prevents accidental exposure of new backend capabilities.
