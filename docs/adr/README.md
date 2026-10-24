# Architecture decision records

One file per decision that was expensive to make and would be expensive to reverse.
Each records the context, the choice, what it costs, and the option that was rejected —
because the rejected option is the part a reader cannot reconstruct from the code.

A record that only argues for what was chosen has documented a conclusion, not a
decision, so the rejected alternative is required.

From here on, records are not rewritten to look consistent in hindsight. A decision that
changes gets a new record, and the old one gains a status line pointing at it. (These
seven were consolidated once, on 2026-10-24, from thirteen earlier records; the originals
are in git history.)

| # | Decision | Status |
|---|---|---|
| [0001](0001-generate-bindings-from-samm.md) | Generate Pydantic bindings from SAMM, checked against the published artefacts | Accepted |
| [0002](0002-rules-as-versioned-data.md) | Rules as versioned data, grounded in the regulation text | Accepted |
| [0003](0003-one-core-asset-profiles-as-data.md) | One asset-agnostic core, asset profiles as data | Accepted |
| [0004](0004-train-in-pytorch-serve-onnx.md) | Train in PyTorch, serve ONNX | Accepted |
| [0005](0005-ship-a-calibrated-interval.md) | Ship a calibrated interval and a drift flag with every estimate | Accepted |
| [0006](0006-verify-llm-citations-in-code.md) | Trust LLM output only through citations verified in code | Accepted |
| [0007](0007-one-container-on-lambda-dynamodb-store.md) | One container on Lambda, DynamoDB behind a repository port | Accepted |
