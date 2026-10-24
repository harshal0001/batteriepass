# 0007 — One container on Lambda, DynamoDB behind a repository port

**Status:** Accepted · **Date:** 2026-09-10, revised 2026-10-24

## Context

Passports must be reachable at a public URL indefinitely. A QR code on a CV or a label is
the product; a link that dies is worse than no link. The deployment budget is zero.

Every free Postgres tier fails the same way: Supabase pauses after a week of inactivity,
Neon suspends on limits. That is fatal for a link scanned twice a year. DynamoDB's
always-free tier has no idle pause, and the access pattern — get a passport by ID — needs
nothing more.

An earlier version of this decision also shipped a Helm chart for Kubernetes and put the
frontend on Vercel. The chart spoke to one ecosystem only, and a second frontend origin
meant a second deployment to keep in step and a CORS policy that had to be right for the
QR page to load at all.

## Decision

**One arm64 container on AWS Lambda behind a Function URL, in `eu-central-1`.** It serves
the API and the built React frontend from the same origin. The Lambda Web Adapter fronts a
plain FastAPI app that knows nothing about Lambda. Reserved concurrency is capped so a
crawler cannot exhaust the free tier, and models load lazily so `/healthz` never loads one.

**DynamoDB, provisioned at 5/5**, inside the always-free tier; on-demand is billed
differently and is not covered the same way.

**The application never talks to `boto3` directly.** `bpass.passport` defines a narrow
repository interface — get, put, and a guard on demo records — with DynamoDB as one
adapter and an in-memory adapter for tests.

**Demo records are protected in the adapter.** Records with `is_demo=true` cannot be
overwritten or deleted, and because the guard sits in the adapter, no route can bypass it.

## Consequences

The test suite runs with no AWS and no Docker. Storage stays reversible: a deployment that
wants Postgres writes a second adapter, not a rewrite. The port stays narrow on purpose;
widening it for relational queries is how it would rot.

One image means one place to measure cold start and image size, and both grow with every
artefact a profile adds, so both are published rather than assumed. The image is an
ordinary HTTP container, so running it on Kubernetes needs a manifest, not an application
change — that is the claim made, and nothing more.

Out of scope: the Eclipse Dataspace Connector and Catena-X onboarding and certification.
The passport is exposed in the Asset Administration Shell submodel shape a connector would
front, so the interface is recognisable without the dataspace plumbing.
