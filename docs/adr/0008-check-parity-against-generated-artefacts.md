# 0008 — Check parity against the published artefacts, not a local Java toolchain

**Status:** Accepted · **Date:** 2026-09-10 · **Amends:** [0002](0002-generate-pydantic-bindings-from-samm.md)

## Context

Record 0002 committed to proving the Python generator against the official Java SAMM
toolchain, on the reasoning that a parser nobody has checked is a claim rather than a
measurement. That reasoning stands. The proposed mechanism was to put a JVM and the
SAMM command-line tool into the build and compare output.

While pinning the aspect models it turned out that `sldt-semantic-models` already
publishes the Java toolchain's output beside every Turtle file. For BatteryPass 6.1.0
that is a generated JSON Schema, a generated example payload, an Asset Administration
Shell submodel template and an OpenAPI document.

Those artefacts are the same reference, already computed, already versioned with the
model they describe, and already covered by the pinning and hashing this project does
anyway.

## Decision

Parity is checked against the published artefacts. Three assertions, in increasing
strength:

1. The official example payload validates against the generated bindings.
2. Dumping it back reproduces the same keys in the same structure — which is the
   claim that every alias, every optional field and every nesting decision is right.
3. That output validates against the official JSON Schema.

The third is the one that matters: it says a Catena-X consumer would accept what this
project produces, judged by the ecosystem's own schema rather than by our reading of
the specification.

The Java toolchain is not vendored, not installed, and not required. The `java` pytest
marker introduced for it is withdrawn.

## Consequences

The check is deterministic, needs no JVM, no network and no container, and runs on
every pull request rather than only where someone has a JDK. It is also pinned: the
reference artefacts are hashed in the same manifest as the Turtle they came from, so
the reference cannot move underneath the test.

The scope narrows honestly. This proves agreement on one aspect model and its example,
not that the generator implements SAMM. That is the correct claim to make, and the
generator raises rather than guessing whenever it meets a construct outside the subset.

Two findings came out of building it, both recorded here because they are the kind of
thing that costs an afternoon to rediscover.

**The published schema declares JSON Schema draft-04**, where `exclusiveMaximum` is a
boolean modifier rather than a numeric bound. Validating it as draft 2020-12 reports
eight errors against the official example payload itself. The test asserts the
declared draft before using it, so a future upstream change to a newer draft fails
loudly instead of silently validating nothing.

**Byte equality is the wrong assertion for `xsd:dateTime`.** XML Schema defines no
canonical width for fractional seconds. The official payload writes `.576` and
Python's `isoformat` writes `.576000`; both are valid lexical forms of the same
instant. Eighteen fields in the example differ this way and no others. The test
asserts that every difference is of exactly that kind, which is a stronger statement
than byte equality would have been and a true one.
