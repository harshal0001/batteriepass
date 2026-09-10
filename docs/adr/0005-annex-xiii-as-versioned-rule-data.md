# 0005 — Annex XIII as versioned rule data

**Status:** Accepted · **Date:** 2026-09-10

## Context

Annex XIII of Regulation (EU) 2023/1542 lists the attributes a battery passport must
carry. That list is not settled. Six of the eight harmonised standards supporting it
were adopted in July 2026; the remaining two are in flight, and the EU DPP Registry
has only been operational since 20 July 2026.

Encoding the list as Python constants would make every rule change a code change, and
would make it impossible for a stored passport to say which reading of the rules it
was checked against.

## Decision

The mandatory attribute list lives in `rulesets/annex-xiii/<version>/` as data. It is
loaded at startup, hashed, and both the version string and the SHA-256 are stamped on
every `ConformanceReport`.

Three rules follow from that.

- **Versions are served side by side.** A passport checked against `2026-07` stays
  checked against `2026-07`. Changing the default is a separate, deliberate commit.
- **A new rule set is never adopted automatically.** Detection and preparation are
  automated; adoption is a human-merged pull request.
- **`scripts/diff_rulesets.py` reports what changed** between two versions: attributes
  added, removed, moved between clusters, or changed from static to dynamic. That
  diff is the body of the pull request.

## Consequences

Rule changes become reviewable rather than archaeological. When a passport is
challenged, the record itself answers "against what?".

The cost is one loader, one hashing step and the discipline never to shortcut it. The
temptation will be to hard-code "just this one attribute" during a late-week push.
That is exactly the change that makes every prior record unauditable.

This mirrors the KoSIT rule-set handling in the XRechnung project, for the same
reason and with the same non-negotiables.
