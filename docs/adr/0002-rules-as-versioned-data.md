# 0002 — Rules as versioned data, grounded in the regulation text

**Status:** Accepted · **Date:** 2026-09-10

## Context

Annex XIII of Regulation (EU) 2023/1542 lists what a battery passport must carry, and
that list is still settling: six of its eight harmonised standards were adopted in July
2026. The engine profile checks record items from Part-M M.A.305, which EASA also revises.

Encoding the rules as Python constants would make every rule change a code change, and
would leave a stored passport unable to say which reading of the rules it was checked
against.

The obvious source for the Annex XIII list is the Catena-X aspect model, whose property
descriptions quote the regulation heavily: 91 property paths carrying 20 distinct
references. It looked complete. It was not. Points 1(f), (i), (j), (m) and (q) are cited
nowhere in it, and 2(b) has no equivalent at all — six of twenty-eight mandatory points
missing, and passports reported conformant that are not.

## Decision

**Rules are data.** Each profile's rule sets live in versioned folders. They are loaded
at startup and hashed, and every conformance result carries the version and SHA-256.

- **Versions are served side by side.** A passport checked against one version stays
  checked against it. Changing the default is a deliberate, human-merged commit; a new
  rule set is never adopted automatically.
- **The regulation text is the source.** It is fetched, extracted verbatim, hashed and
  committed, as the aspect models are. For Annex XIII the **consolidated** EUR-Lex text
  is used: point 1(q) was corrected after publication, and the original would encode a
  superseded requirement.
- **Grounded and editorial statements are kept apart.** Parsed from the regulation, never
  typed: identifier, verbatim text, access level, scope. Editorial and marked as such:
  cluster, passport paths, and how long a dynamic field may go unrefreshed. Annex XIII
  groups by *who may read* the information; the seven clusters group by subject, and
  that reading is ours.
- **Each rule carries a digest of its own text**, whitespace-collapsed and case-folded so
  a markup reflow is not mistaken for an amendment. A real wording change makes the
  loader refuse the rule set until the mapping is reviewed again.
- **An unmappable point is kept and reported, not dropped.** Point 2(b) is the live case.
- **Every mapped path is checked against the generated schema**, not a payload, so a path
  that addresses nothing after an upstream model change fails as a mapping bug instead of
  looking like missing data.

## Consequences

The Annex XIII list is provably complete: 28 points — 19 in Part 1, 4 in Part 2, one
dashed item in Part 3, 4 in Part 4. Tests assert those counts from the pinned text.

The cost is one loader, one hashing step, and the discipline never to hard-code "just
this one attribute". That is the change that would make every prior record unauditable.
