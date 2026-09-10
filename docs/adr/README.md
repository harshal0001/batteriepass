# Architecture decision records

One file per decision that was expensive to make and would be expensive to reverse.
Each records the context at the time, the choice, and what it costs — including the
option that was rejected, because the rejected option is the part a reader cannot
reconstruct from the code.

Records are immutable once merged. A decision that changes gets a new record that
supersedes the old one; the old one stays, marked superseded. A decision log that is
edited to look consistent in hindsight is not a log.

| # | Decision | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-generate-pydantic-bindings-from-samm.md) | Generate Pydantic bindings from SAMM in Python | Accepted |
| [0003](0003-train-in-pytorch-serve-onnx.md) | Train in PyTorch, serve ONNX | Accepted |
| [0004](0004-dynamodb-behind-a-repository-port.md) | DynamoDB, behind a repository port | Accepted |
| [0005](0005-annex-xiii-as-versioned-rule-data.md) | Annex XIII as versioned rule data | Accepted |
| [0006](0006-ship-a-calibrated-interval.md) | Ship a calibrated interval with every estimate | Accepted |
| [0007](0007-two-deployment-targets.md) | Two deployment targets: Lambda and Helm | Accepted |
