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

## 2026-10-26 — Conformance checker

**Built:** `conform/check.py`: `check(passport, ruleset, now) → ConformanceReport`. The
rule-set loader now refuses a dynamic rule without a refresh interval, and
`DynamicFieldState.last_refreshed_at` may be `None` (unknown → stale). Design doc first:
`docs/design/conformance-checker.md`.

**Patterns / concepts used:** conformance check (presence), dynamic field (freshness),
pure function with the clock passed in (glossary).

**Decisions made:** the five presence rules in the design doc §4.4: all paths of a rule,
at least one list item, empty is absent, freshness from the passport's own timestamps,
missing items named by rule id + paths. No ADR: they are editorial, like the cluster
mapping, and live beside the code that applies them.

**Diagrams added/updated:** `docs/design/conformance-checker.md` (components, rule flow),
`docs/ARCHITECTURE.md` (module map node).

**What I (owner) understood well:** …

**What the agent decided that I did not review:** naive timestamps read as UTC (marked
`shortcut:` in `check.py`); the official example scores 27/28 with all four dynamic fields
stale, which is correct but means no demo passport is conformant yet.

**Open questions / things I don't understand yet:**
- The binding enforces 35 of 37 rule paths on its own. Is the checker then mostly
  redundant for batteries, and what changes when the aspect model relaxes a field?
- 4(c) (battery status) has no timestamp in BatteryPass, so it is always stale. Should a
  rule set be able to name a fallback timestamp, e.g. `metadata.lastModification`?

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
