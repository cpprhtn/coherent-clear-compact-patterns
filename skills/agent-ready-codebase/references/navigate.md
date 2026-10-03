# Navigate
Locate: root index.md → (child card only if its children line matches) → source. Use search when no card matches.

Build or fix cards:
- `python scripts/cards.py <repo>` → missing, stale, broken links, unreachable cards. Exit 1 = issues.
- Derive cards from code and tests only, never from a pending task.
- Write only what the repo doesn't already show (`assets/card.md`). No generic overviews or style rules the code already reveals.
- Claude Code: one line in root CLAUDE.md — "Module contracts live in the root index.md. Read it first; edit it only when one of its lines becomes false." Nothing else.

After edits: update the nearest card; if children changed, update the parent line.
