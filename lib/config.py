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


def cmd_get(args: list[str]) -> int:
    if not args:
        print("usage: config.py get <dotted.key>", file=sys.stderr)
        return 2
    key = args[0]
    defaults = _load_yaml(_plugin_dir() / "config.defaults.yaml")
    value = _get(defaults, key)
    if value is None:
        print(f"key not defined: {key}", file=sys.stderr)
        return 1
    print(_format(value))
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: config.py <get|show|validate|init|doctor> [args]", file=sys.stderr)
        return 2
    verb, *rest = sys.argv[1:]
    if verb == "get":
        return cmd_get(rest)
    print(f"unknown verb: {verb}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
