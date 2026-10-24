# 0005 — Ship a calibrated interval and a drift flag with every estimate

**Status:** Accepted · **Date:** 2026-09-10, revised 2026-10-24

## Context

State of health and remaining useful life cannot be measured; they are estimated. A bare
point estimate — `soh_percent: 87.3` — reads as a measurement. Rendered on a public
passport next to fields that *are* measurements, it will be read as equally solid, and
resale, warranty and maintenance decisions get made on numbers like it.

The failure is quiet. A model applied to a chemistry or operating condition it never saw
does not fail loudly; it returns a confident wrong number. Worse, a conformal interval's
guarantee holds only when the input resembles the calibration data, so on exactly those
inputs the band keeps its usual width while its coverage collapses.

## Decision

**The point estimate is the mean of a five-seed ensemble.**

**Every estimate carries a split-conformal prediction interval**, calibrated on held-out
units (cells or engines never used in training). The record publishes both the nominal
coverage requested and the empirical coverage delivered: a nominal 90% band that covers
71% is worse than no band, and only the second number reveals it. The interval may be
scaled by ensemble spread, but spread only scales a calibrated quantile; it is never the
interval itself.

**Every request is checked for drift.** Per-feature reference distributions from training
ship beside the model as `drift_reference.json`. Each request computes a PSI or KS
statistic per feature; above the threshold, the estimate is stored with
`in_distribution = false` and the features that triggered it, and the page shows it as
unreliable.

**Certification is denied explicitly.** `certified` is typed `Literal[False]`, so a JSON
consumer sees the claim denied rather than merely absent, and every model card states
the non-certified status in its first paragraph.

The rejected alternatives were a softmax-style confidence or a predicted-variance head,
both miscalibrated under distribution shift, and a learned out-of-distribution detector,
which is one more model to calibrate and cannot name the input that triggered it.

## Consequences

Conformal prediction needs no change to architecture or training loop. The cost is a
larger held-out budget, since calibration units cannot also be test units, and five ONNX
files per profile instead of one.

Intervals will sometimes be embarrassingly wide on the transfer sets. That is the point.

The drift thresholds are a judgement, so they are tested against evidence: on the
cross-chemistry and cross-condition sets, the flag must fire where measured coverage falls
below target, and if it does not, that is reported. Per-feature tests miss shifts that
show only in combinations of features; that limit is accepted for a flag whose reason a
reader can check.
