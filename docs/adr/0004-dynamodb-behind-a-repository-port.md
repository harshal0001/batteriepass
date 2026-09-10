# 0004 — DynamoDB, behind a repository port

**Status:** Accepted · **Date:** 2026-09-10

## Context

Passports must be retrievable at a public URL indefinitely. The QR codes printed in
a README, on a CV, or on a physical label are the product; a link that dies is worse
than no link.

Every free Postgres tier has the same failure mode. Supabase pauses a project after
a week of inactivity. Neon suspends on limits. Both are fine for a service with
traffic and fatal for a demo link that gets scanned twice a year.

DynamoDB's always-free tier — 25 GB storage and 25 provisioned read and write
capacity units — has no idle-pause behaviour. It simply keeps working.

The access pattern is also trivially suited to it: a passport is a single-item
`GetItem` by ID. There is no join, no scan, no query that needs anything more.

## Decision

DynamoDB in `eu-central-1`, provisioned at 5/5 — well inside the free ceiling, and
provisioned rather than on-demand because on-demand is billed differently and is not
covered the same way.

**But the application never talks to `boto3` directly.** `bpass.passport` defines a
repository interface and DynamoDB is one adapter behind it. An in-memory adapter
backs the test suite.

## Consequences

The port costs one small module and buys three things.

The test suite runs with no AWS and no Docker, which keeps the feedback loop fast.
The choice becomes reversible: a Catena-X deployment that wants Postgres writes a
second adapter rather than a rewrite. And the storage decision stops leaking into
the API layer, which is what makes the module boundaries in this repo real rather
than decorative.

The cost is that a document store's shape is not hidden by the port. Anything that
wanted a relational query would need the port widened, and widening it is how this
abstraction would rot. It stays narrow: get, put, and a guard on demo records.

Demo passports carry `is_demo=true` and the store refuses to overwrite or delete
them. That flag is enforced in the adapter, not in the API, so no route can bypass it.
