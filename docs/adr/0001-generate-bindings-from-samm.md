# 0001 — Generate Pydantic bindings from SAMM, checked against the published artefacts

**Status:** Accepted · **Date:** 2026-09-10

## Context

Every passport schema in this project is a SAMM aspect model in RDF Turtle: Catena-X's
`io.catenax.battery.battery_pass` for batteries, and an `EngineHealthPass` model written
for this project for engines. The official SAMM toolchain generates **Java**. There is
no Python path.

Three options existed.

1. **Hand-write the Pydantic models.** Fastest to start, and wrong the first time
   Catena-X publishes a revision — silently, because nothing compares the two.
2. **Run the Java SAMM CLI and translate its output.** A JVM in the build and two
   generators to keep honest instead of one.
3. **Write a Python generator.** Parse the Turtle with `rdflib`, walk properties,
   characteristics, enumerations and constraints, and emit typed Pydantic v2 models
   with the semantic URN preserved on every field.

## Decision

Option 3, scoped to the subset of SAMM the project's aspect models use. A complete SAMM
implementation is not the deliverable. The generator knows RDF, not any asset.

- **Generated output is committed and never hand-edited.** CI regenerates and fails on
  any diff.
- **An unsupported construct raises.** The generator never emits `Any`; bindings that
  typecheck and lie are worse than a build that stops.
- **Parity is checked against the published artefacts, not a local Java toolchain.**
  `sldt-semantic-models` publishes the Java toolchain's output beside every Turtle file —
  a JSON Schema and an example payload among them — already versioned with the model
  and covered by the same pinning and hashing. Three assertions, in increasing strength:
  1. The official example payload validates against the generated bindings.
  2. Dumping it back reproduces the same keys in the same structure.
  3. That output validates against the official JSON Schema — a Catena-X consumer would
     accept it, judged by the ecosystem's own schema.

## Consequences

The check is deterministic, needs no JVM and no network, and runs on every pull request.
It proves agreement on one aspect model and its example, not that the generator
implements SAMM; that is the claim made.

Writing the engine's aspect model ourselves makes it tempting to stay inside what the
generator already handles. The engine model is written from the domain first; anything
it needs that the generator lacks is implemented, or the generator raises.

Two findings, recorded because they cost an afternoon to rediscover:

- **The published schema declares JSON Schema draft-04**, where `exclusiveMaximum` is a
  boolean modifier. Validated as draft 2020-12 it reports eight errors against the
  official example itself. The test asserts the declared draft before using it.
- **Byte equality is the wrong assertion for `xsd:dateTime`.** The official payload
  writes `.576` and Python writes `.576000`; both are valid forms of the same instant.
  Eighteen fields differ this way and no others, and the test asserts exactly that.
