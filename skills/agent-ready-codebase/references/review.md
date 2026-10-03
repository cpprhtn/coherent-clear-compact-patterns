# Review
Report to the human:
CONTRACT: signature / behavior / effect semantics — each unchanged | changed | unknown
EVIDENCE: which tests or checks cover each unchanged claim; missing coverage stated
TESTS: commands run, pass/fail, tests added, tests changed or weakened
FOCUS: file:line + reason, ordered by risk

Rules:
- Never say review is unnecessary. At most propose a narrower scope, with the evidence that justifies it.
- "unchanged" needs evidence; without it write "unknown".
- Request full review if the change touches security, concurrency, transactions, error handling, persistence formats, or retries, or if any CONTRACT item is unknown.
- Report test deletions, skips, or loosened asserts explicitly.
- Never report pass without running tests.
- Flag imports outside the card's deps.
Length follows risk; don't cut a risk to stay short.
