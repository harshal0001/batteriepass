# 0003 — One asset-agnostic core, asset profiles as data

**Status:** Accepted · **Date:** 2026-10-24

## Context

The project was built for one asset, a lithium-ion battery, and its core types say so:
`Cluster` lists the seven Annex XIII clusters, `ConformanceReport` refuses any report
that does not cover exactly those seven, and `SoHEstimate` holds a state of health.

The service now has a second asset, the turbofan engine. The hard parts are the same for
both: generated bindings, rules as versioned data, a degradation model with an interval,
cited extraction, cited regulation answers. What differs is data.

There is no EU engine passport mandate. The engine profile's rules come from
continuing-airworthiness record-keeping, Part-M M.A.305, and it makes no airworthiness
determination. A design that pretended otherwise would discredit the battery half.

## Decision

The core knows no asset. Each asset is a **profile**: a folder under `profiles/<name>/`
holding its aspect models, rule sets, model artefacts, extraction schema and corpus.
A profile contains data and artefacts, never code.

- **Rule sets declare their own clusters.** The core keeps the guard that every cluster is
  reported, because an omitted cluster reads as a pass, but the list comes from the rule
  set being checked. `Cluster` and `ANNEX_XIII_CLUSTERS` leave `core/`.
- **One health type for both assets.** `SoHEstimate` becomes `HealthEstimate` with a
  `target` of `soh_percent` or `rul_cycles`, keeping everything [0005](0005-ship-a-calibrated-interval.md)
  requires.
- **A `Profile` enum names the profiles.** It is the one line of code a new profile costs,
  and it keeps a misspelt profile out of stored records.
- **The engine profile cites its paragraph.** Every M.A.305 check names the paragraph it
  implements, as every Annex XIII rule names its point.

The rejected alternatives were a second repository, which duplicates every hard part, and
`if profile == ...` branches in the core, which make a third asset a code change in every
module.

## Consequences

The battery's pinned sources move under `profiles/battery/`, and the loader, fetch scripts
and tests follow. The pinning, hashing and CI checks do not change.

Every type that crosses the core is now judged by whether it means the same thing for a
cell and an engine. That is a useful test, and occasionally an inconvenient one.
