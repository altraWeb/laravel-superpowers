#!/usr/bin/env python3
"""laravel-superpowers config helper.

Reads merged YAML config from defaults + user-global + per-project layers
and exposes simple CLI verbs for hooks to query.
"""
import os
import sys
from pathlib import Path

import yaml


def _plugin_dir() -> Path:
    """Resolve the plugin root from $CLAUDE_PLUGIN_ROOT (set by Claude Code)."""
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not root:
        # Fallback: assume this file lives at <plugin>/lib/config.py
        return Path(__file__).resolve().parent.parent
    return Path(root)


def _load_yaml(path: Path) -> dict:
    """Load a YAML file. Returns empty dict if missing."""
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _get(data: dict, dotted_key: str):
    """Look up a value via dot-notation. Returns None if missing."""
    cur = data
    for part in dotted_key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _format(value) -> str:
    """Format a value for stdout: bool->lowercase, list->JSON, else str."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        import json
        return json.dumps(value)
    return str(value)


def _user_config_path() -> Path:
    return Path(os.environ["HOME"]) / ".claude" / "plugins" / "altraweb-laravel" / "laravel-superpowers" / "config.yaml"


def _project_config_path() -> Path:
    return Path.cwd() / ".laravel-superpowers.yaml"


def _deep_merge(base: dict, overlay: dict) -> dict:
    """Recursively merge overlay into a copy of base. Overlay wins on conflicts."""
    result = dict(base)
    for key, val in overlay.items():
        if isinstance(val, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def _merged_config() -> dict:
    """Return defaults merged with user overlay, then project overlay."""
    defaults = _load_yaml(_plugin_dir() / "config.defaults.yaml")
    user = _load_yaml(_user_config_path())
    project = _load_yaml(_project_config_path())
    return _deep_merge(_deep_merge(defaults, user), project)


def cmd_get(args: list[str]) -> int:
    if not args:
        print("usage: config.py get <dotted.key>", file=sys.stderr)
        return 2
    key = args[0]
    value = _get(_merged_config(), key)
    if value is None:
        print(f"key not defined: {key}", file=sys.stderr)
        return 1
    print(_format(value))
    return 0


def _load_schema() -> dict:
    import json
    return json.load(open(_plugin_dir() / "config.schema.json"))


def cmd_validate(args: list[str]) -> int:
    """Validate one config file (path arg) or all three layers (no args)."""
    from jsonschema import validate as js_validate, ValidationError

    schema = _load_schema()

    if args:
        paths = [Path(args[0])]
    else:
        paths = [
            _plugin_dir() / "config.defaults.yaml",
            _user_config_path(),
            _project_config_path(),
        ]

    had_error = False
    for path in paths:
        if not path.exists():
            continue
        try:
            data = _load_yaml(path)
        except yaml.YAMLError as e:
            print(f"YAML parse error in {path}: {e}", file=sys.stderr)
            had_error = True
            continue
        try:
            js_validate(data, schema)
        except ValidationError as e:
            location = ".".join(str(p) for p in e.absolute_path) or "<root>"
            print(f"schema violation in {path} at {location}: {e.message}", file=sys.stderr)
            had_error = True

    return 3 if had_error else 0


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: config.py <get|show|validate|init|doctor> [args]", file=sys.stderr)
        return 2
    verb, *rest = sys.argv[1:]
    dispatch = {"get": cmd_get, "validate": cmd_validate}
    if verb not in dispatch:
        print(f"unknown verb: {verb}", file=sys.stderr)
        return 2
    return dispatch[verb](rest)


if __name__ == "__main__":
    sys.exit(main())
