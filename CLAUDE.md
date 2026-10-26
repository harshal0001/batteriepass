# Agent instructions — Asset Health Passport

> Read by the coding agent (Claude Code, Codex, Cursor…) at the start of every session.
> It is the contract between the project owner and the agent. The owner's goal is to
> **understand and learn from everything that gets built**, and to keep the system
> **robust, scalable and well-architected**. Everything here applies unless the owner
> overrides it in chat.

---

## 0. Project facts

- **Project:** Asset Health Passport (`batteriepass`). Standards-based digital passports
  for degrading assets: EV batteries (EU Battery Regulation 2023/1542) and turbofan
  engines (EASA Part-M), sharing one asset-agnostic core. Full description: `README.md`.
- **Language / runtime:** Python 3.12 (`>=3.12,<3.13`), managed with `uv`.
- **Frameworks:** FastAPI + Pydantic v2 (serving), rdflib (code generation only),
  ONNX Runtime (inference), PyTorch (training only, in `training/`), structlog,
  pydantic-settings, boto3 (DynamoDB only). Frontend planned: React + TypeScript + Vite.
- **Datastore:** DynamoDB behind a repository port (ADR-0007).
- **Commands:**
  - install: `uv sync --all-extras`
  - test: `uv run pytest`
  - lint / format / types: `uv run ruff check src tests scripts` ·
    `uv run ruff format --check src tests scripts` · `uv run mypy src/bpass`
  - serving-boundary guard: `uv run python scripts/no_torch_in_src.py`
  - pinned-source checks: see "Local development" in `README.md`
- **Deployment target:** one arm64 container on AWS Lambda (Function URL) + DynamoDB,
  `eu-central-1`. Scales to zero; **cold start is the governing constraint**.
- **Expected scale:** research / portfolio project. Low request volume, bursty (QR scans).
  Deployment budget: zero. Design for correctness and traceability first, cold start
  second, throughput last.
- **Non-negotiables:** the ten in `README.md` → "Non-negotiables". They are enforced by
  tests and CI. Never weaken a guard to make a change pass; raise it with the owner.

---

## 1. Prime directive: teach while building

The owner builds with agents daily and cannot learn *and* build at the same time. Make
learning a by-product of building:

1. **Explain before you implement.** For any non-trivial task, describe the 2–3 viable
   approaches with trade-offs, recommend one, and **wait for the owner's choice** unless
   told "just do it".
2. **Design docs before code.** Any feature touching more than one module under
   `src/bpass/`, any new external dependency, any data-model or profile-schema change,
   gets a design doc in `docs/design/` **before** implementation
   (`uv run python scripts/new_design.py "<feature>"`). At least one Mermaid diagram.
3. **Record decisions as ADRs** in the project's existing style (`docs/adr/README.md`):
   Context, Decision, Consequences, and the **rejected alternative is required**.
   `uv run python scripts/new_adr.py "<title>"`. Never rewrite an accepted ADR; add a
   new one and give the old one a status line pointing at it.
4. **Keep the architecture map current.** `README.md` holds the public-facing diagrams.
   `docs/ARCHITECTURE.md` holds the engineering map (module inventory, cross-cutting
   concerns, scale notes). When a module, dependency, table or external call appears,
   update `docs/ARCHITECTURE.md` in the same PR, and the README diagram if the
   high-level picture changed.
5. **Maintain the glossary.** The first time you introduce a pattern or domain term
   (conformal prediction, PSI, repository port, aspect model, idempotency key…), add it to
   `docs/glossary.md` with a 2–3 line explanation and a link to where it lives in this
   repo.
6. **Write to the learning log.** At the end of a session append to `docs/LEARNINGS.md`:
   what was built, which patterns were used, what the owner did not review. When asked
   to "explain", answer from this codebase with file references and a diagram.

---

## 2. Diagrams

Mermaid in fenced blocks, so diagrams live in git and render on GitHub. Pick by question:

| Question | Diagram |
|---|---|
| Who calls whom, in what order? | `sequenceDiagram` |
| What are the branches in this logic? | `flowchart` |
| What are the big boxes and how do they connect? | `flowchart` with `subgraph`s |
| What are the entities and relations? | `erDiagram` |
| What states can this thing be in? | `stateDiagram-v2` |
| What types exist and how do they relate? | `classDiagram` |

One diagram answers one question; ≤ 10 nodes. Cheat sheet: `docs/diagrams.md`.

---

## 3. Architecture & code principles

The project already follows these; keep it that way. Where a principle is overkill for
the stated scale, say so and record the simplification as an ADR.

### Structure (as it stands — do not blur these lines)
- `core/` is the domain contract: depends only on Pydantic, strict mypy, no I/O.
- `samm/` knows RDF, not assets. `conform/` knows rules, not transport.
  `passport/` assembles and persists. `api/` is transport only.
- `bindings/` is generated and never hand-edited. `profiles/` is data, never logic.
- `training/` is the only place `torch` is imported. CI enforces this.
- Dependencies point inward: `api` → `passport`/`conform` → `core`. Infrastructure
  (DynamoDB, ONNX session, LLM client) sits behind an interface defined inward.
- Every non-trivial module starts with a short comment on **why** it exists and where it
  sits, as the existing modules and `pyproject.toml` already do.

### Robustness
- Validate at boundaries (HTTP, file loaders, profile loaders). Pydantic models at the
  edge; the loaders already refuse unknown constructs rather than emit `Any`. Keep that.
- Typed exceptions in `core/`, mapped to HTTP status codes in `api/`. Distinguish
  "expected" (unknown profile, non-conformant passport) from "unexpected" (bug, AWS down).
- Every outbound call (DynamoDB, LLM API, model load) has a timeout. Retries only for
  idempotent operations, with backoff and jitter.
- Writes are idempotent: passport records keyed deterministically, re-POST returns the
  existing record.
- Structured logs (structlog, already a dependency) with a request id on every entry.
- Config via pydantic-settings and environment; secrets never in the repo.
- Provenance is a feature, not logging: `model_sha256`, `ruleset_sha256`, page + quote.

### Scalability (within the Lambda shape)
- Stateless handlers; nothing in process memory survives beyond a warm instance except
  read-only artefacts (ONNX session, rule set, embedding index) loaded once at import.
- Everything added to the serving image is weighed against cold start. Name the size.
- Pagination on any list endpoint. DynamoDB access patterns designed before the table.
- Slow or third-party work (document extraction, embedding) is a candidate for a
  separate step, not the QR-scan request path.
- Before closing a feature answer: **what breaks at 10× and 100× QR-scan traffic, and
  what would we change?**

### Optimisation
- Measure first. "Measured so far" in the README only contains numbers from real runs;
  keep it that way.
- Avoid N+1 against DynamoDB; batch where the SDK allows.

### Testing
- Test plan written in the design doc first ("what could break?").
- Unit tests for `core/` and `conform/` (no I/O); property-based tests (Hypothesis) where
  a round-trip exists, as `tests/samm/` already does; `aws`-marked tests against
  DynamoDB Local; one end-to-end test per passport flow.

---

## 4. Workflow for every task

1. **Understand**: restate the task; list assumptions and unknowns; ask if a wrong guess
   is expensive.
2. **Plan**: options → trade-offs → recommendation → wait (use plan mode if available).
3. **Document**: design doc and/or ADR per §1.
4. **Implement** in small steps. Commit messages explain *why*, in the style of the
   existing history.
5. **Test** per the plan; run the full CI command set from §0 locally.
6. **Update** `docs/ARCHITECTURE.md`, `docs/glossary.md`, README diagrams if needed.
7. **Close**: scale question (§3), `docs/LEARNINGS.md` entry, short summary with
   pointers to the docs touched.

---

## 5. Communication

- Lead with the decision or result, then the reasoning.
- New concept → one-line definition → why it matters here → where it lives in the code.
- Flag uncertainty. Never invent an API; check the dependency's docs or source.
- Push back when a request conflicts with §3 or the README non-negotiables.
- Never silently skip a §4 step; say "skipping design doc: one-line fix" when justified.

---

## 6. Repository conventions

```
CLAUDE.md / AGENTS.md         this contract
README.md                     public face: purpose, diagrams, stack, non-negotiables
docs/
  ARCHITECTURE.md             engineering map, kept current
  LEARNINGS.md                session learning log
  glossary.md                 terms → where used
  diagrams.md                 Mermaid cheat sheet
  adr/                        decision records (project style, see adr/README.md)
  design/                     per-feature design docs
scripts/
  new_adr.py · new_design.py · check_docs.py     documentation helpers
  (existing fetch/build/guard scripts unchanged)
.claude/commands/             /design /adr /explain /onboard /scale-review /learnings
.github/workflows/
  ci.yml                      existing: lint, types, tests, pinned-source guards
  docs-check.yml              new: source changed ⇒ docs changed; Mermaid parses
```
