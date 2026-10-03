# Audit
1. `python scripts/cards.py <repo>` → card sync signals (not proof of correctness).
2. `python scripts/cards.py <repo> --cochange` → modules often changed together; a lead to inspect, not proof of coupling.
3. `python scripts/prefix.py <repo>` → fixed prefix per request; if `.claude/settings.json` has no tool manifest, apply references/compact.md.
4. Sample 3 modules: does each card state behavior and effects the code doesn't reveal, and are they true? Check write.md rules 2–5.

Report per axis (Coherent, Clear, Compact): finding, evidence, confidence. Then top 3 fixes by impact ÷ effort, each with the risk it adds.
