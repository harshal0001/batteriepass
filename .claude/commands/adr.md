---
description: Record an architecture decision in this project's ADR style
---

Write an ADR for the decision: $ARGUMENTS

This project has an established ADR style; read `docs/adr/README.md` and one existing
record (e.g. `docs/adr/0004-train-in-pytorch-serve-onnx.md`) first and match it.

Steps:
1. Run `uv run python scripts/new_adr.py "$ARGUMENTS"` to create the next numbered file
   from `docs/adr/0000-template.md`. It also appends an index row.
2. Fill **Context** with the situation and the concrete numbers or constraints (cold start,
   budget, traceability, the README non-negotiables) that make the obvious option untenable.
3. Fill **Decision**: what we do and how it is *enforced* (test, CI step, type), not
   intended. Add a small before/after Mermaid diagram if structure changes.
4. Fill **Consequences**: what it costs, what it buys, and **the rejected alternative and
   why it lost**. A record without the rejected alternative is incomplete.
5. Add a short **Learning notes** paragraph for the owner; add new terms to `docs/glossary.md`.
6. If this changes an earlier decision, add `**Status:** Superseded by NNNN` to the old
   record's status line; never rewrite its body.
7. Show me Context, Decision and the rejected alternative, and ask whether to mark it
   Accepted (and update the index row).
