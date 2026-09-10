# 0006 — Ship a calibrated interval with every estimate

**Status:** Accepted · **Date:** 2026-09-10

## Context

Annex XIII requires state of health as a dynamic field. State of health cannot be
measured directly; it is estimated. The regulation asks for a number and offers no
way to produce one, which is the reason this project has a model at all.

A bare point estimate — `soh_percent: 87.3` — reads as a measurement. It is not one.
Rendered on a public passport page next to manufacturing site and chemistry, which
*are* measurements, it will be read as equally solid. That is a real harm, not a
presentational quibble: resale value and warranty decisions get made on this number.

The literature makes the problem concrete. Cross-chemistry generalisation is the open
problem in this field. A model trained on LFP fast-charge cells at 30 °C and applied
to a different chemistry does not fail loudly; it returns a confident wrong number.

## Decision

Every estimate carries a distribution-free prediction interval from split conformal
prediction, calibrated on held-out cells.

The record publishes both the nominal coverage that was requested and the empirical
coverage the calibration set actually delivered. A nominal 90% band that covers 71%
of held-out cells is worse than no band, and only the second number reveals it.

`SoHEstimate.certified` is typed `Literal[False]`. It cannot be set true. It exists so
that a consumer reading the JSON sees the claim denied rather than merely absent.

The model card states the non-certified status in its first paragraph, and is written
before the API, not after.

## Consequences

Conformal prediction is cheap: one calibration split, one quantile, no change to the
architecture or the training loop. The cost is a wider held-out budget, since
calibration cells cannot also be test cells.

The interval will sometimes be embarrassingly wide, particularly on the NASA and
Oxford transfer sets. That is the point. A wide band on out-of-distribution
chemistry is the model reporting the thing a point estimate would hide.

The rejected alternative was a softmax-style confidence or a model-predicted variance
head. Both are miscalibrated under distribution shift, which is precisely the regime
this model will be used in.
