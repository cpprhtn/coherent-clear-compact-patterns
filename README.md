# coherent-clear-compact-patterns

**Coherent for agents. Clear for reviewers. Compact in tokens.**

Code design patterns that work for both AI agents and humans: agents handle the code correctly, humans review it easily, and it costs few tokens. What gets judged is the code written in the pattern, not the agent's workflow.

> This is not about building AI systems. It is about the code AI agents work on.

## 3C

Three criteria for judging a pattern. Each question is about code written in the pattern.

| Criterion | Question | For |
|---|---|---|
| **Coherent** | Does an agent understand and explain it correctly, and fix or extend it without breaking existing behavior? | AI agents |
| **Clear** | Can a human review the code and its changes fast and without missing bugs? | Reviewers |
| **Compact** | Does the pattern keep the code short, so agents read and write few tokens (input first, output too)? | Cost |

A 3C pattern helps all three together: no criterion worse, at least one better. A pattern that saves tokens but hides risk, or helps one criterion at another's expense, is a trade-off, not a 3C pattern.

3C are criteria, not a pattern. Every pattern here stays a candidate until measured.

## What is known so far

- **Tokens are mostly fixed overhead.** In Claude Code, 83–96% of an agent's input tokens on short tasks are the prompt prefix (system prompt + tool definitions) re-sent on every request. Input ≈ prefix × requests.
- **A tool manifest cuts that overhead.** A committed `.claude/settings.json` that denies built-in tools the repo never uses cut input tokens to about 0.37× and cost to about 0.60× on short tasks, less on longer sessions. It is an environment default, not a code pattern. A small loss in pass rate on hard tasks could not be ruled out, so check your own tests after adding one.
- **Repo docs for agents do not save tokens.** Contract cards (`index.md`) did not reduce tokens or cost in any tested design; each extra file to read adds a request. Use them for contracts, not for cost.
- **Code structure patterns are not yet tested.** Whether a structure (for example, modules grouped by what changes together, or a functional core with an imperative shell) helps all three criteria is the open question.

## The skill: `agent-ready-codebase`

A Claude skill that applies these practices. It is a tool for applying patterns, not proof that they work.

| Part | What it does |
|---|---|
| Contract card (`assets/card.md`) | One flat `index.md` at the repo root holding only what code doesn't show: behavior, invariants, effect semantics |
| Review report (`references/review.md`) | The agent reports by contract (unchanged / changed / unknown, with evidence), tests run, and where to look first |
| Compact setup (`references/compact.md`, `assets/settings.tools-min.json`) | Tool manifest template and the order of token levers |
| `scripts/prefix.py <repo>` | Measures the fixed prompt prefix in a repo (one small `claude -p` call) |
| `scripts/cards.py <repo>` | Checks cards for sync problems: missing or oversized cards, broken or missing links, cards older than their source |

Install for Claude Code:

```bash
git clone https://github.com/cpprhtn/coherent-clear-compact-patterns.git
cp -r coherent-clear-compact-patterns/skills/agent-ready-codebase ~/.claude/skills/
```

For one project only, copy it to `<project>/.claude/skills/` instead.

## Related work

Meng & Jackson, *What You See Is What It Does* (Onward! 2025) · Gloaguen et al., *Evaluating AGENTS.md* (ICML 2026) · Trivedi & Schmitt, *Does Code Cleanliness Affect Coding Agents?* (2026) · Ousterhout, *A Philosophy of Software Design*. Patterns for building agentic AI systems are a different topic.

## License

MIT (see `LICENSE`).
