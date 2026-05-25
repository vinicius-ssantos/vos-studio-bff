from app.tool_policy import is_allowed, normalize_role, policy_catalog, tool_min_role, tool_policy


def test_normalize_role_defaults_to_viewer():
    assert normalize_role("admin") == "admin"
    assert normalize_role(" operator ") == "operator"
    assert normalize_role("unknown") == "viewer"


def test_low_risk_tools_are_viewer_accessible():
    policy = tool_policy("status")

    assert policy.known is True
    assert policy.risk == "low"
    assert policy.min_role == "viewer"
    assert is_allowed("status", "viewer") is True


def test_medium_risk_tools_require_operator_or_admin():
    policy = tool_policy("create_creative_sprint")

    assert policy.known is True
    assert policy.risk == "medium"
    assert policy.min_role == "operator"
    assert is_allowed("create_creative_sprint", "viewer") is False
    assert is_allowed("create_creative_sprint", "operator") is True
    assert is_allowed("create_creative_sprint", "admin") is True


def test_unknown_tools_are_blocked_by_default():
    policy = tool_policy("new_backend_capability")

    assert policy.known is False
    assert policy.risk == "unknown"
    assert tool_min_role("new_backend_capability") == "admin"
    assert is_allowed("new_backend_capability", "admin") is False
    assert is_allowed("new_backend_capability", "viewer", block_unknown_tools=False) is True


def test_policy_catalog_is_sorted_and_grouped():
    catalog = policy_catalog()

    assert "status" in catalog["low"]
    assert "create_client" in catalog["medium"]
    assert catalog["low"] == sorted(catalog["low"])
    assert catalog["medium"] == sorted(catalog["medium"])
    assert catalog["high"] == []
