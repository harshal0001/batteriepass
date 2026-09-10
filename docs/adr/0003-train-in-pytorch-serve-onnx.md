# 0003 — Train in PyTorch, serve ONNX

**Status:** Accepted · **Date:** 2026-09-10

## Context

The passport needs a state-of-health number on the request path. The obvious shape
is one program: train a PyTorch model, load the checkpoint in the API, call it.

The numbers make that shape untenable on the target platform. A CPU-only `torch`
install is roughly 700 MB. `onnxruntime` is roughly 50 MB. The service runs as a
Lambda container that scales to zero, so that difference is paid on every cold start,
and a cold start is the first thing anyone who scans the QR code experiences.

## Decision

Training and serving are different programs with different dependencies on different
machines. Training uses PyTorch on a Kaggle GPU. Serving uses ONNX Runtime on a
Lambda CPU. The only artefact that crosses the boundary is a `.onnx` file plus its
metadata.

`torch` is never imported under `src/`. `scripts/no_torch_in_src.py` enforces it in
CI by parsing every module and by reading the runtime dependency list.

Export is not trusted on faith. `training/export.py` runs 1,000 held-out samples
through both PyTorch and ONNX Runtime and asserts `max |Δ| < 1e-4`. The parity test
is committed and runs in CI against committed reference outputs.

## Consequences

Two dependency sets to maintain, and a model change is a two-step release: export,
then verify parity, then deploy.

In exchange the image stays small, the cold start stays measurable, and the training
environment is free to use whatever it likes without touching production.

The rejected alternative was serving PyTorch on a larger, always-warm instance. It
costs money, and the whole deployment budget for this project is zero.

An exported model that silently diverges from the one that was evaluated is worse
than no export at all, which is why the parity assertion is a hard failure rather
than a warning.
