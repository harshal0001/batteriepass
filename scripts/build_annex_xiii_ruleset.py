#!/usr/bin/env python3
"""Build the Annex XIII rule set from the pinned regulation text.

Two kinds of statement go into a rule and they are not equally grounded, so the
build keeps them apart — the same discipline the XRechnung project applies to
explanations, for the same reason.

**Grounded.** The point's identifier, its verbatim text, its access level and whether
it describes the battery model or an individual battery. All parsed out of
``annex-xiii.txt``, which is fetched from EUR-Lex and hashed. Never typed here.

**Editorial.** Which of the seven reporting clusters a point belongs to, which paths
in the passport satisfy it, and whether it is a dynamic field. Annex XIII organises
itself by *who may read the information*, not by subject, so the seven clusters are a
reading imposed on top of it. That reading lives in MAPPING below, is marked as
editorial in the output, and is reviewable line by line.

Each rule carries a digest of its own regulation text. When the text changes, the
digest changes, the rule is flagged, and its mapping needs re-review. A rule set that
silently keeps a stale mapping against amended text is worse than one that stops.

    python scripts/build_annex_xiii_ruleset.py --version 2025-07-31
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULESETS = REPO / "rulesets" / "annex-xiii"

# Access level and scope per part, from the part headings in the annex itself.
PARTS: dict[int, tuple[str, str]] = {
    1: ("public", "model"),
    2: ("legitimate_interest", "model"),
    3: ("notified_bodies", "model"),
    4: ("legitimate_interest", "individual"),
}

# --- editorial: the seven-cluster reading and the passport path mapping ------
#
# cluster, paths into the BatteryPass aspect model, dynamic, note.
#
# `dynamic` marks a field that must be refreshed through the battery's life rather
# than fixed at manufacture. Every one of them is in Part 4, which is the part about
# an individual battery rather than the model — that alignment is the regulation's,
# not ours.
MAPPING: dict[str, tuple[str, tuple[str, ...], bool, str]] = {
    "1.a": (
        "general",
        ("identification.identification.type", "operation.manufacturer", "identification.category"),
        False,
        "Annex VI Part A is the general battery information block: manufacturer, "
        "category, place and date of manufacture, weight and capacity.",
    ),
    "1.b": (
        "materials",
        ("identification.chemistry", "materials.hazardous", "materials.composition"),
        False,
        "",
    ),
    "1.c": ("carbon_footprint", ("sustainability.carbonFootprint",), False, ""),
    "1.d": ("due_diligence", ("conformity.dueDiligencePolicy",), False, ""),
    "1.e": ("materials", ("materials.composition.recycled",), False, ""),
    "1.f": ("materials", ("materials.composition.renewable",), False, ""),
    "1.g": ("performance_durability", ("performance.rated.capacity",), False, ""),
    "1.h": ("performance_durability", ("performance.rated.voltage",), False, ""),
    "1.i": ("performance_durability", ("performance.rated.power",), False, ""),
    "1.j": ("performance_durability", ("performance.rated.lifetime",), False, ""),
    "1.k": (
        "performance_durability",
        ("performance.rated.capacity.thresholdExhaustion",),
        False,
        "Electric-vehicle batteries only. Absence is not a gap for other categories; "
        "the engine reads identification.category before requiring it.",
    ),
    "1.l": ("performance_durability", ("performance.rated.temperature",), False, ""),
    "1.m": ("performance_durability", ("characteristics.warranty",), False, ""),
    "1.n": ("performance_durability", ("performance.rated.roundTripEfficiency",), False, ""),
    "1.o": ("performance_durability", ("performance.rated.resistance",), False, ""),
    "1.p": (
        "performance_durability",
        ("performance.rated.lifetime.cycleLifeTesting.appliedChargeRate",),
        False,
        "",
    ),
    "1.q": (
        "compliance",
        ("safety.meaningOfLabels", "identification.idDmc"),
        False,
        "Carries a corrigendum marker in the consolidated text: the Official Journal "
        "wording of this point was corrected after publication.",
    ),
    "1.r": ("compliance", ("conformity.declarationOfConformity",), False, ""),
    "1.s": (
        "circularity",
        ("sustainability.documents.separateCollection", "sustainability.documents.wastePrevention"),
        False,
        "",
    ),
    "2.a": ("materials", ("materials.active",), False, ""),
    "2.b": (
        "materials",
        (),
        False,
        "No path. BatteryPass 6.1.0 models no part numbers for components or contact "
        "details for replacement spares. An unmapped mandatory point is reported as "
        "such rather than quietly dropped — see ADR 0009.",
    ),
    "2.c": ("circularity", ("safety.dismantling",), False, ""),
    "2.d": ("circularity", ("safety.safetyMeasures",), False, ""),
    "3.-": (
        "compliance",
        ("conformity.resultOfTestReport",),
        False,
        "Part 3 has no lettered points: it is a single dashed item.",
    ),
    "4.a": (
        "performance_durability",
        ("performance.dynamic.capacity.capacity", "performance.dynamic.power.remaining"),
        True,
        "Refreshed when the battery is placed on the market and on every change of status.",
    ),
    "4.b": (
        "performance_durability",
        ("performance.dynamic.capacity.fade",),
        True,
        "State of health. This is the field the model estimates: it cannot be measured "
        "directly, and without it the passport is incomplete.",
    ),
    "4.c": ("circularity", ("sustainability.status",), True, ""),
    "4.d": (
        "performance_durability",
        (
            "performance.dynamic.fullCycles",
            "performance.dynamic.negativeEvents",
            "performance.dynamic.operatingEnvironment",
            "performance.dynamic.stateOfCharge",
        ),
        True,
        "",
    ),
}

# How often a dynamic field is expected to be refreshed before it reads as stale.
# Editorial: the regulation says these must be kept up to date and sets no interval.
DEFAULT_MAX_AGE_DAYS = 365


def parse_annex(text: str) -> list[dict[str, object]]:
    """Parse the annex into (part, point, verbatim text).

    The extracted layout puts each marker on its own line — ``1.``, ``(a)``, ``—`` —
    followed by its body. Corrigendum markers (``▼C4``, ``▼B``) sit between entries
    and are structural noise rather than content.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    rules: list[dict[str, object]] = []
    part: int | None = None
    point: str | None = None
    body: list[str] = []

    def flush() -> None:
        if part is not None and point is not None and body:
            rules.append({"part": part, "point": point, "text": " ".join(body).strip()})

    for line in lines:
        if line.startswith("▼"):
            continue
        part_match = re.fullmatch(r"([1-4])\.", line)
        if part_match:
            flush()
            part, point, body = int(part_match.group(1)), None, []
            continue
        point_match = re.fullmatch(r"\(([a-z])\)", line)
        if point_match:
            flush()
            point, body = point_match.group(1), []
            continue
        if line == "—" and part == 3 and point is None:
            flush()
            point, body = "-", []
            continue
        if part is not None and point is not None:
            body.append(line)

    flush()
    return rules


def digest(text: str) -> str:
    """Digest of the regulation text, whitespace-collapsed and case-folded.

    Collapsed so that a reflow in the EUR-Lex markup does not read as an amendment.
    Case-folded for the same reason. Anything that survives both is a real change.
    """
    normalised = re.sub(r"\s+", " ", text).strip().casefold()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:16]


def build(version: str) -> dict[str, object]:
    directory = RULESETS / version
    source = directory / "annex-xiii.txt"
    if not source.is_file():
        raise SystemExit(f"error: {source} not found. Run scripts/fetch_annex_xiii.py first.")

    parsed = parse_annex(source.read_text(encoding="utf-8"))
    if not parsed:
        raise SystemExit("error: parsed no rules out of the annex text")

    rules = []
    unmapped = []
    for entry in parsed:
        key = f"{entry['part']}.{entry['point']}"
        if key not in MAPPING:
            unmapped.append(key)
            continue
        cluster, paths, dynamic, note = MAPPING[key]
        access, scope = PARTS[int(entry["part"])]  # type: ignore[arg-type]
        rule: dict[str, object] = {
            "id": f"XIII.{key}",
            "part": entry["part"],
            "point": entry["point"],
            "text": entry["text"],
            "text_digest": digest(str(entry["text"])),
            "access": access,
            "scope": scope,
            "cluster": cluster,
            "paths": list(paths),
            "dynamic": dynamic,
        }
        if dynamic:
            rule["max_age_days"] = DEFAULT_MAX_AGE_DAYS
        if note:
            rule["note"] = note
        rules.append(rule)

    if unmapped:
        raise SystemExit(
            f"error: the annex text contains points with no entry in MAPPING: "
            f"{', '.join(unmapped)}. Every mandatory point must be mapped or explicitly "
            f"recorded as unmappable."
        )

    stale = sorted(set(MAPPING) - {f"{r['part']}.{r['point']}" for r in rules})
    if stale:
        raise SystemExit(
            f"error: MAPPING has entries the annex text does not contain: {', '.join(stale)}. "
            f"The regulation may have been amended."
        )

    return {
        "version": version,
        "regulation": "Regulation (EU) 2023/1542",
        "annex": "XIII",
        "$comment": (
            "Generated by scripts/build_annex_xiii_ruleset.py from the pinned annex text. "
            "The id, text, access and scope of every rule are parsed from the regulation. "
            "The cluster, paths and dynamic flag are an editorial reading and are reviewable."
        ),
        "clusters": sorted({str(rule["cluster"]) for rule in rules}),
        "rules": rules,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="2025-07-31")
    parser.add_argument("--check", action="store_true", help="fail if the committed file is stale")
    args = parser.parse_args(argv)

    built = build(args.version)
    destination = RULESETS / args.version / "ruleset.json"
    rendered = json.dumps(built, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not destination.is_file():
            print(f"error: {destination} is missing", file=sys.stderr)
            return 1
        if destination.read_text(encoding="utf-8") != rendered:
            print(
                f"error: {destination.relative_to(REPO)} does not match a fresh build. "
                f"Run scripts/build_annex_xiii_ruleset.py and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"Rule set matches a fresh build ({len(built['rules'])} rules).")  # type: ignore[arg-type]
        return 0

    destination.write_text(rendered, encoding="utf-8")
    rules = built["rules"]
    dynamic = sum(1 for rule in rules if rule["dynamic"])  # type: ignore[union-attr,index]
    print(f"wrote {destination.relative_to(REPO)}: {len(rules)} rules, {dynamic} dynamic")  # type: ignore[arg-type]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
