# Glossary

> The agent adds an entry the first time it introduces a pattern or domain term.
> Format: **Term** — 2–3 line explanation → where it lives in this repo. Alphabetical.

**AAS (Asset Administration Shell)** — Industry 4.0 standard for a digital twin's
information model; a passport is exposed as an AAS *submodel* so a dataspace connector
could sit in front of it. → `README.md` "Out of scope"; `aas-core3.0` in the stack

**ADR (Architecture Decision Record)** — One file per expensive-to-reverse decision:
context, decision, consequences, and the rejected alternative. → `docs/adr/`

**Annex XIII** — The annex of Regulation (EU) 2023/1542 listing the mandatory battery
passport attributes (28 points, seven clusters, with public / restricted access levels).
Encoded as versioned data, not constants. → `profiles/battery/rulesets/annex-xiii/`, ADR-0002

**Aspect model (SAMM)** — Catena-X's Semantic Aspect Meta Model: an RDF/Turtle schema
describing a data payload. The project generates Pydantic bindings from it rather than
hand-writing types. → `profiles/battery/samm-models/`, `src/bpass/samm/`, ADR-0001

**Catena-X** — The automotive dataspace whose semantic models define the battery passport
payload (`io.catenax.battery.battery_pass`). Pinned by commit hash. → `profiles/battery/samm-models/sources.json`

**Cold start** — Time for a scaled-to-zero Lambda to load its image and import its code
before serving the first request. The size of the serving image is the main lever; the
reason `torch` is excluded. → `pyproject.toml` comments, ADR-0004, ADR-0007

**Conformal prediction (split)** — A distribution-free method that turns any point
predictor into an interval with a guaranteed coverage (e.g. 90%) by calibrating on a
held-out set. Ships with every health estimate. → ADR-0005

**Deep ensemble** — Several models trained from different random seeds; the spread of
their predictions is a cheap, strong uncertainty estimate. Five seeds here. → ADR-0005, `training/`

**Drift flag (PSI / KS)** — Per-feature comparison of a request's inputs against a stored
training reference using the Population Stability Index or Kolmogorov–Smirnov test; if
inputs look unlike training data the estimate is marked unreliable. → ADR-0005

**Generated code, byte-stable** — Code emitted by a generator and committed; CI
regenerates it and fails on any diff, so a hand edit cannot survive. → `src/bpass/bindings/`, `bpass.samm.generate --check`

**Hexagonal / ports and adapters** — Business logic in the centre with no framework
imports; infrastructure (DynamoDB, ONNX, LLM) reached through interfaces ("ports") that
adapters implement. → `docs/ARCHITECTURE.md` §1, ADR-0007 (repository port)

**Idempotency** — An operation that can be repeated safely with the same effect as doing
it once; required for anything that may be retried. → `CLAUDE.md` §3 (planned for passport POST)

**ONNX / ONNX Runtime** — Open Neural Network Exchange: a portable model file format and
a small CPU inference runtime (~50 MB vs ~700 MB for CPU torch). Only `.onnx` files cross
from training to serving. → ADR-0004

**Pinned source + manifest** — Upstream artefacts (aspect models, regulation text) are
fetched once, hashed, committed with a manifest, and verified offline in CI so they
cannot change silently. → `scripts/fetch_samm.py --check`, `scripts/fetch_annex_xiii.py --check`

**Profile** — A folder of data and artefacts for one asset type (aspect model, rule set,
ONNX model, extraction schema, regulation corpus). Holds data, never logic. → `profiles/`, ADR-0003

**Provenance** — The record of where every number came from: `model_sha256`,
`ruleset_version` + `ruleset_sha256`, and page + verbatim quote for extracted fields. → ADR-0005, ADR-0006

**Repository port** — The interface the application layer uses to store and load records,
implemented by a DynamoDB adapter (and a fake in tests). → ADR-0007

**RUL / SoH** — Remaining Useful Life (cycles or time left) and State of Health
(% of original capacity). The two health figures a passport carries. → `README.md`

**Split by unit** — Train/validation/test splits are made by physical unit (cell, engine),
never by time step, so no unit leaks across splits. → `README.md` non-negotiable 5

**Verified citation** — An LLM-extracted field is kept only if its quoted text is found on
the cited page and the value matches; otherwise it is dropped, never guessed. → ADR-0006

<!-- Suggested future entries when they appear in code: single-table design (DynamoDB),
request id / correlation id, circuit breaker, outbox, QLoRA, embedding index, PSI. -->
