# 0004 — Train in PyTorch, serve ONNX

**Status:** Accepted · **Date:** 2026-09-10

## Context

Every passport needs a health number on the request path. The obvious shape is one
program: train a PyTorch model, load the checkpoint in the API, call it.

The numbers make that untenable. A CPU-only `torch` install is roughly 700 MB;
`onnxruntime` is roughly 50 MB. The service runs as a Lambda container that scales to
zero, so the difference is paid on every cold start — the first thing anyone who scans
the QR code experiences.

## Decision

Training and serving are different programs with different dependencies on different
machines. Training uses PyTorch on a Kaggle GPU. Serving uses ONNX Runtime on a Lambda
CPU. Only `.onnx` files and their metadata cross the boundary.

`torch` is never imported under `src/`. `scripts/no_torch_in_src.py` enforces it in CI
by parsing every module and reading the runtime dependency list.

Export is not trusted on faith: held-out samples run through both PyTorch and ONNX
Runtime and must agree to `max |Δ| < 1e-4`, as a hard failure rather than a warning.

## Consequences

Two dependency sets to maintain, and a model change is a release in steps: export, verify
parity, deploy. In exchange the image stays small and the training environment can use
whatever it likes without touching production.

The rejected alternative was serving PyTorch on a larger, always-warm instance. It costs
money, and the deployment budget for this project is zero.
