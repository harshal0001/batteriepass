# 0002 — Generate Pydantic bindings from SAMM in Python

**Status:** Accepted · **Date:** 2026-09-10

## Context

Catena-X aspect models — including `io.catenax.battery.battery_pass`, the schema of
record for this project — are published as SAMM instances in RDF Turtle in
`eclipse-tractusx/sldt-semantic-models`. The official toolchain generates **Java**
classes from them. There is no Python path.

Three options existed.

1. **Hand-write the Pydantic models.** Fastest to start. The aspect model has well
   over a hundred properties across seven clusters, and it is versioned upstream: a
   hand-written copy is wrong the first time Catena-X publishes a revision, and
   wrong silently, because nothing compares the two.
2. **Run the Java SAMM CLI and translate its output.** Correct by construction, but
   it puts a JVM in the build and produces Java, which then needs a second
   translation step to reach Pydantic. Two generators to keep honest instead of one.
3. **Write a Python generator.** Parse the Turtle with `rdflib`, walk the SAMM
   properties, characteristics, enumerations and constraints, emit typed Pydantic v2
   models with the semantic URN preserved on every field.

## Decision

Option 3. Scoped deliberately to the subset of SAMM the BatteryPass model actually
uses — a complete SAMM implementation is not the deliverable and would not finish.

Two things make it trustworthy rather than merely convenient:

- **Generated output is committed and never hand-edited.** CI regenerates and fails
  on any diff, so the rule is enforced rather than requested.
- **Parity against the official Java toolchain is a test.** The same aspect model
  goes through both generators and the serialised output must match. Without that,
  "I wrote a SAMM parser" is a claim; with it, it is a measurement.

## Consequences

The generator is the single most defensible piece of engineering in the project,
because it fills a gap that genuinely exists in the ecosystem rather than
re-implementing something already available.

It also means SAMM features outside the BatteryPass subset are unsupported, and the
generator must say so loudly — an unsupported construct raises, it never silently
emits `Any`. A generator that quietly degrades is worse than one that refuses.

The Java parity test needs a JVM and the SAMM CLI, which not every contributor has.
It is marked `java` in pytest and skipped when the CLI is absent, but it runs in CI.
