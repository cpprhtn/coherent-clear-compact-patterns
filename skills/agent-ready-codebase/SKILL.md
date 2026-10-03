---
name: agent-ready-codebase
description: Use when you change, refactor, or review code in a repo that has an index.md contract card, or when asked to create or fix one. A card holds the contract code doesn't show; opening it first and reporting changes by contract keeps work correct and reviewable. Also use when the user mentions AI-friendly architecture, agent token cost, setting up a repo for coding agents, or reviewability.
---

# Agent-Ready Codebase (3C)

Goal (3C), judged on the code itself: Coherent (agents understand and explain it correctly, and fix or extend it without breaking existing behavior; what changes together lives together), Clear (a human reviews the code and its changes fast and without missing bugs), Compact (the pattern doesn't make the code long, so agents read and write few tokens; input first, output too). A good pattern helps all three together; one that wins on one axis and loses on another is a trade-off. Less context is not a win if it hides risk.

Tokens: input ≈ fixed prefix (system prompt + tool definitions) × requests. Cards don't save tokens (measured cost-neutral at best); a tool manifest does (references/compact.md). Use cards for contracts, not for cost.

## Contract card
Default: ONE flat `index.md` at the repo root holding the contract code alone doesn't show (behavior, invariants, effect semantics). Never restate what code, types, or README already say. Add child cards only when the root card would exceed its budget. Format and budget: `assets/card.md` (read only when writing a card).

## Read only what the task needs
| Task | Read |
|---|---|
| Write or refactor code | references/write.md, then references/review.md for the report |
| Review a diff | references/review.md |
| Locate code, build or fix cards | references/navigate.md |
| Assess a codebase | references/audit.md |
| Cut agent token cost, set up a repo for agents | references/compact.md |

## Always
- Open the root card, follow a child link only if one matches the target, then open source at the target. Fall back to search when the card doesn't match.
- Edit a card only when the change makes one of its lines false or adds a contract it should state. If every line stays true, leave the card untouched.
- Card contradicts code: code wins. Fix the card, tell the user.
