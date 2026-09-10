# 0007 — Two deployment targets: Lambda and Helm

**Status:** Accepted · **Date:** 2026-09-10

## Context

The service has two audiences and they want to see different things.

Anyone scanning the QR code wants a page that loads. That argues for the cheapest
always-available hosting that exists, which is a Lambda container behind a Function
URL with a static frontend on Vercel. Total cost zero, no idle billing, no pause.

Anyone from the Catena-X ecosystem wants to know how this would run in their
environment. Every Tractus-X reference application — `digital-product-pass`,
`tractusx-edc`, the Digital Twin Registry — ships a Helm chart and runs on
Kubernetes. A Lambda-only deployment answers a question they did not ask.

## Decision

Both, from one image.

- **Lambda container + Function URL** is the live demo. arm64 for Graviton, 1024 MB,
  reserved concurrency capped so a crawler cannot burn the free tier, CORS restricted
  to the Vercel origin, ONNX session loaded lazily so `/healthz` answers immediately.
- **A Helm chart** deploys the same image to Kubernetes, with a `kind` quickstart in
  the README. It is not deployed anywhere permanently; it exists to be read and to be
  run locally in one command.

The application knows about neither. It is a FastAPI app listening on a port; the
Lambda Web Adapter translates events to HTTP in front of it, and Kubernetes does not
need to translate anything.

## Consequences

The Helm chart costs about a day and must be kept honest — a chart that does not
deploy is worse than no chart, so CI lints it and runs a `kind` install.

Explicitly out of scope: the Eclipse Dataspace Connector, Catena-X network onboarding
and certification. Those are months of work and none of it is engineering that shows
anything new. What is in scope instead is exposing the passport in the Asset
Administration Shell submodel-descriptor shape that a connector would front, so the
interface is recognisable even though the dataspace plumbing is absent.
