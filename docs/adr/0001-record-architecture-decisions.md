# 0001 — Record architecture decisions

**Status:** Accepted · **Date:** 2026-09-10

## Context

This project sits on top of two moving targets. Regulation (EU) 2023/1542 becomes
enforceable on 18 February 2027 and six of its eight harmonised standards were only
adopted in July 2026. The Catena-X aspect models it binds to are versioned upstream
and change without warning. Decisions taken now will be read later by someone —
possibly me in six months — who no longer remembers what the alternatives were.

The failure mode is specific: a reader sees the code, infers a reason, and the
inferred reason is wrong. They then "fix" something that was deliberate.

## Decision

Every decision that is expensive to reverse gets a numbered record in `docs/adr/`
stating the context, the choice, the rejected alternative and the cost.

Records are immutable after merge. A superseded decision keeps its file and gains a
status line pointing at the record that replaced it.

## Consequences

Writing one costs about fifteen minutes. Not writing one costs an afternoon of
archaeology later, or a silent regression when someone removes a constraint that
looked arbitrary.

A rejected alternative is a required section. A record that only argues for what was
chosen has documented a conclusion, not a decision.
