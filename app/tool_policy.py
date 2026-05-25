from dataclasses import dataclass
from typing import Literal

Role = Literal["viewer", "operator", "admin"]
RiskLevel = Literal["low", "medium", "high", "unknown"]

_ROLE_RANK: dict[str, int] = {"viewer": 0, "operator": 1, "admin": 2}

_LOW_RISK_TOOLS = {
    "status",
    "get_sprint_status",
    "list_sprint_assets",
    "get_video_job_status",
    "list_video_jobs",
    "search_library",
}

_MEDIUM_RISK_TOOLS = {
    "create_client",
    "save_brand_kit",
    "create_creative_sprint",
    "prepare_dashboard_pack",
    "register_manual_asset",
    "record_asset_performance",
    "record_performance_metrics",
    "promote_to_library",
}

_HIGH_RISK_TOOLS: set[str] = set()


@dataclass(frozen=True)
class ToolPolicy:
    name: str
    risk: RiskLevel
    min_role: Role | None
    known: bool


def normalize_role(role: str) -> Role:
    normalized = role.strip().lower()
    if normalized == "admin":
        return "admin"
    if normalized == "operator":
        return "operator"
    return "viewer"


def tool_policy(tool_name: str) -> ToolPolicy:
    if tool_name in _HIGH_RISK_TOOLS:
        return ToolPolicy(name=tool_name, risk="high", min_role="admin", known=True)
    if tool_name in _MEDIUM_RISK_TOOLS:
        return ToolPolicy(name=tool_name, risk="medium", min_role="operator", known=True)
    if tool_name in _LOW_RISK_TOOLS:
        return ToolPolicy(name=tool_name, risk="low", min_role="viewer", known=True)
    return ToolPolicy(name=tool_name, risk="unknown", min_role=None, known=False)


def tool_min_role(tool_name: str) -> Role:
    return tool_policy(tool_name).min_role or "admin"


def is_allowed(tool_name: str, role: str, *, block_unknown_tools: bool = True) -> bool:
    policy = tool_policy(tool_name)
    if not policy.known:
        return not block_unknown_tools

    normalized_role = normalize_role(role)
    min_role = policy.min_role or "admin"
    return _ROLE_RANK[normalized_role] >= _ROLE_RANK[min_role]


def policy_catalog() -> dict[str, list[str]]:
    return {
        "low": sorted(_LOW_RISK_TOOLS),
        "medium": sorted(_MEDIUM_RISK_TOOLS),
        "high": sorted(_HIGH_RISK_TOOLS),
    }
