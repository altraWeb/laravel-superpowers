"""Tests for lib/config.py."""


def test_get_returns_default_value(cli):
    """With no user/project overlay, `get` returns the default."""
    result = cli("get", "pilot_version")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "2"


def test_get_nested_key_via_dot_notation(cli):
    result = cli("get", "hook_enabled.banned_token_leak_guard")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "true"


def test_get_unknown_key_exits_1(cli):
    result = cli("get", "nonexistent")
    assert result.returncode == 1
    assert "key not defined" in result.stderr


def test_get_list_returns_json_array(cli):
    result = cli("get", "banned_tokens.exception_paths")
    assert result.returncode == 0, result.stderr
    import json
    parsed = json.loads(result.stdout)
    assert "CHANGELOG.md" in parsed


def test_user_overlay_overrides_default(cli, user_config_dir):
    (user_config_dir / "config.yaml").write_text("pilot_version: 1\n")
    result = cli("get", "pilot_version")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "1"
