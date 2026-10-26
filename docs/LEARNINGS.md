# Learning log

> Appended at the end of every working session (the agent drafts, the owner edits).
> Newest at the top. `/learnings` generates an entry. The **Open questions** lines are the
> most valuable: start the next session with `/explain <one of them>`.

---

## YYYY-MM-DD — <session title>

**Built:** …

**Patterns / concepts used:** <term> (glossary), <term> (glossary)

**Decisions made:** ADR-NNNN

**Diagrams added/updated:** `docs/design/…`, `docs/ARCHITECTURE.md`, `README.md`

**What I (owner) understood well:** …

**What the agent decided that I did not review:** …

**Open questions / things I don't understand yet:**
- …

---

## 2026-10-26 — Retrofitted the learning/architecture template

**Built:** `CLAUDE.md` contract adapted to this project; `docs/ARCHITECTURE.md`
engineering map; ADR template in the project's own style; design-doc template and index;
glossary seeded with the project's domain and pattern vocabulary; Mermaid cheat sheet;
slash commands; `scripts/new_adr.py`, `new_design.py`, `check_docs.py`; `docs-check`
workflow; PR template.

**State of the codebase at retrofit:** `core/`, `samm/`, `conform/`, `bindings/` and the
battery profile are built and CI-guarded. `passport/` and `api/` are scaffolds. Health
service, document extraction and regulation Q&A are not started. Seven ADRs exist and
already explain the big decisions.

**Suggested reading order to understand what exists** (about an hour):
1. `README.md` top to "Where the rules come from" — the picture.
2. ADR-0003 → 0001 → 0002 → 0004 → 0005 → 0006 → 0007 (order in `docs/ARCHITECTURE.md` §8).
3. `pyproject.toml` comments and `.github/workflows/ci.yml` comments — every guard has
   its reason written next to it.
4. `src/bpass/samm/generate.py` and `tests/samm/test_parity.py` — how "generated, never
   hand-edited" is actually enforced.

**Open questions to resolve with `/explain` before building further:**
- How does `conform/paths.py` resolve a passport path against the generated schema, and
  what happens when the aspect model changes?
- Where exactly will the repository port live and what does the DynamoDB single-table
  layout look like? (Needs a design doc before `passport/` grows.)
- How will split conformal calibration be computed and stored (`calibration.json`), and
  how is the 90% interval applied at serve time?
- What is the request-id / logging story for a Lambda Function URL with FastAPI?

**Next design docs, in order:** passport creation flow → DynamoDB layout → health
service → document extraction → regulation Q&A.
