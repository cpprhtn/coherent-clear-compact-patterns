# Compact
Measured (Claude Code, 1,440 runs): in short tasks 83–96% of an agent's input tokens are the fixed prefix (system prompt + tool definitions) re-sent on every model request. Input ≈ prefix × requests + what the session accumulates. Repo docs barely change the prefix, and each extra read adds a request. A tool manifest cut input to 0.37× on short tasks, 0.45× on hard ones and 0.60× for a model that takes ~24 tool calls per task: the longer the session, the smaller the share the prefix holds. Hidden-test pass rates matched overall (hard tasks: 84/90 with and without it), but a sealed run could not rule out a loss of up to 10 points, so check your own tests after adding a manifest. So the levers are, in order:

1. **Shrink the prefix with a tool manifest.** Commit `.claude/settings.json` that denies built-in tools this repo's work never needs (`assets/settings.tools-min.json`: keeps Read, Edit, Write, Bash).
   - Measure before and after: `python scripts/prefix.py <repo>` (one tiny `claude -p` call, prints the prefix in tokens).
   - Keep every tool the team actually uses (MCP servers, web search, sub-agents). Project deny rules apply to everyone and cannot be re-allowed locally; for personal use put them in `.claude/settings.local.json` instead.
   - Re-check after CLI upgrades: tool names and the prefix change between versions. Unknown names in the list are harmless.
2. **Don't add requests.** Every file an agent is told to read costs one more prefix. Do not add mandatory reading (cards, guides) for the sake of tokens; even on top of a manifest a flat card raised cost ~10%. Cards are for contracts that prevent wrong changes.
3. Content trimming (shorter cards, shorter CLAUDE.md) moves input by well under 1%. Don't spend effort there for tokens.

Report the effect as measured: prefix before/after, requests per task, input and cost per task, and test pass rate for the same tasks. Fewer tokens with lost tests is not a win.
