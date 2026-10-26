---
description: Write a design doc (with diagrams) for a feature BEFORE implementing it
---

Create a design doc for: $ARGUMENTS

Steps:
1. Read `CLAUDE.md` §0 (project facts) and `docs/ARCHITECTURE.md` so the design fits the existing system.
2. Run `uv run python scripts/new_design.py "$ARGUMENTS"` to create the file from the template, then fill every section:
   - Problem, constraints, assumptions to confirm
   - At least 2 options in the comparison table with a clear recommendation
   - A `flowchart` of components touched and a `sequenceDiagram` of the main flow (plus an `erDiagram` if data changes)
   - Error handling table, robustness checklist, scale review (10× / 100×), test plan, rollout, learning notes
3. If the design involves choosing between alternatives, also create an ADR via `uv run python scripts/new_adr.py` in the project style (`docs/adr/README.md`: Context, Decision, Consequences, rejected alternative required).
4. Add any new term to `docs/glossary.md`.
5. **Stop and present the design to me for approval. Do not write implementation code yet.** Summarise the recommendation in 3 lines and list the assumptions I need to confirm.
