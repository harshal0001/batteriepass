# 0009 — Ground the rule set in the regulation text, and mark the rest editorial

**Status:** Accepted · **Date:** 2026-09-10 · **Refines:** [0005](0005-annex-xiii-as-versioned-rule-data.md)

## Context

Record 0005 decided that the Annex XIII attribute list is versioned data rather than
constants. It did not say where the data comes from.

The obvious source is the Catena-X aspect model, which is already pinned and whose
property descriptions quote the regulation extensively. Extracting those citations
gave 91 property paths carrying 20 distinct Annex XIII references, which looked like
a complete list.

It was not. Checked against the regulation itself, five points of Part 1 — (f), (i),
(j), (m) and (q) — are not cited anywhere in the aspect model's documentation, and
Part 2(b) has no equivalent in the model at all. An attribute list built from the
aspect model alone would have been missing six mandatory points out of twenty-eight
and would have reported passports as conformant that are not.

The second problem is that Annex XIII does not organise itself the way this project
reports. The regulation groups information by **who may read it** — public, persons
with a legitimate interest, notified bodies. The seven clusters this project reports
against group by **subject**. That mapping is a reading, and it is ours.

## Decision

The regulation text is fetched from EUR-Lex, extracted verbatim, hashed and committed
as source data, exactly as the aspect models are. `scripts/fetch_annex_xiii.py` does
it; `--check` verifies offline in CI.

The **consolidated** text is used, not the original Official Journal text. Point 1(q)
carries a corrigendum marker: its published wording was corrected after publication.
Checking against the uncorrected original would encode a superseded requirement.

Every rule then separates two kinds of statement.

**Grounded, parsed from the regulation and never typed by hand:** the point's
identifier, its verbatim text, its access level and whether it describes the battery
model or an individual battery.

**Editorial, and marked as such:** which of the seven clusters the point belongs to,
which passport paths satisfy it, and how long a dynamic field may go unrefreshed.

Each rule carries a digest of its own regulation text. The text is whitespace-collapsed
and case-folded first, so a reflow in the published markup is not mistaken for an
amendment. A real wording change makes the digest disagree with the recorded one, and
the loader refuses the rule set until the mapping has been looked at again.

A mandatory point with no passport path is **kept and reported as unmapped**, not
dropped. Point 2(b) is the live case.

## Consequences

The list is now provably complete against the regulation: twenty-eight points, nineteen
in Part 1 ending at (s), four in Part 2, one dashed item in Part 3, four in Part 4.
Tests assert those counts from the pinned text rather than from the loader.

Every path is checked to resolve against the generated bindings, which catches the
failure this mapping is most likely to suffer. The aspect model is versioned upstream;
a path valid in BatteryPass 6.1.0 may address nothing in the next release, and an
unresolvable path would count as a permanently missing attribute while looking like a
data problem rather than a mapping bug.

The cost is that the editorial layer is genuinely editorial. The cluster assignments
are defensible but they are a judgement, and the rule set says so in every entry
rather than presenting them as if the regulation had made them.
