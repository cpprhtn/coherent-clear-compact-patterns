# Write
1. Read the target card first: purpose, api, and any non-obvious behavior, invariants, effects. Write or fix the card first only when the task creates a new module.
2. Keep the external interface small. Inside, keep code that changes and is read together in one place. Split a file only when it shrinks change scope, reading cost, or coupling. Line counts are signals, not targets.
3. At module boundaries, make dependencies and effects explicit (parameters, not hidden globals). Inside, expose only what the change needs to understand.
4. Prefer data + functions over deep class trees when the language allows; keep idioms (traits, plugins, framework lifecycles) where they carry the contract.
5. Keep effects at the edges where practical. Record each effect's semantics in the card.
6. Name the steps of long flows so the sequence reads top-down.
7. Tie each contract item to a test; list the path in the card.

Done = tests pass, every card line still true (edit only lines the change made false), report written per review.md.
