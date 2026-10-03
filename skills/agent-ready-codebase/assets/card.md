# <module or repo>
purpose: <one line>
covers: <all = this one card covers the whole repo; omit when child cards exist>
api: <public entry points; signatures only if types don't show them>
behavior: <defaults, boundaries, error meaning — only non-obvious ones>
invariants: <what must always hold>
effects: <none | effect + semantics: transaction scope, ordering, idempotency, retries>
modules: <only for a dir with many files: one line per file, contract only; tag the verifying test as [test_x.py]>
deps: <only import rules the code doesn't show, e.g. lazy imports that break cycles>
tests: <path → which line above it verifies>
children:
- <dir>/ — <one-line purpose>

Budget: write a line only if an agent unaware of it would plausibly make a wrong change. Target ≤ 25 lines per leaf card, ≤ ~1.5k tokens for a whole card set; per-module lines, not per-function. Omit a field when it would only restate the code. Never drop a real contract item to fit the budget: split it into a child card instead.
Default layout: a single root card with `covers: all` (no other cards needed). Large repos only: parent cards = purpose + children, test and container dirs = purpose only.
