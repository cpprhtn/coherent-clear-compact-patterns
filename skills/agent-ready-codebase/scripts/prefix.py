#!/usr/bin/env python3
"""Measure the fixed prompt prefix Claude Code sends on every request in a repo (system prompt + tool definitions + CLAUDE.md).
Usage: prefix.py <repo> [--model claude-sonnet-5-5]
Runs one tiny non-interactive request with project settings only and prints its input tokens and the tools the model sees.
Costs one small request. Compare before/after a tool manifest (.claude/settings.json)."""
import json, subprocess, sys

repo = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "claude-sonnet-5-5"
r = subprocess.run(["claude", "-p", "--model", model, "--setting-sources", "project", "--strict-mcp-config",
                    "--output-format", "json", "--max-budget-usd", "1"],
                   input="List the exact names of every tool you have, comma separated, nothing else.",
                   cwd=repo, capture_output=True, text=True)
try:
    j = json.loads(r.stdout)
except json.JSONDecodeError:
    sys.exit("claude failed: " + (r.stderr or r.stdout)[-300:])
u = j.get("usage") or {}
total = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
print(f"prefix_tokens: {total}")
print(f"tools: {j.get('result', '').strip()}")
