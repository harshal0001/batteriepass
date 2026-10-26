"""Judge one passport against one rule set.

Presence, not correctness: this answers whether a passport *carries* each mandatory point.
Types are the generated bindings' job; whether the values are true is out of scope.

Rule paths are payload names, so the passport is dumped by alias and walked as plain data.
That the paths exist in the schema at all is proven separately, in CI, by ``paths.py``.
The presence rules are an editorial reading, recorded in docs/design/conformance-checker.md.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime

from pydantic import BaseModel

from bpass.conform.ruleset import Rule, Ruleset
from bpass.core import ClusterCoverage, ConformanceReport, DynamicFieldState


def check(passport: BaseModel, ruleset: Ruleset, now: datetime) -> ConformanceReport:
    """Per-cluster coverage and dynamic-field freshness. Pure: ``now`` is passed in."""
    payload = passport.model_dump(by_alias=True)

    missing: dict[str, list[str]] = {cluster: [] for cluster in ruleset.clusters}
    dynamic: list[DynamicFieldState] = []

    for rule in ruleset.rules:
        absent = [path for path in rule.paths if not _present(payload, path.split("."))]
        if not rule.paths:
            missing[rule.cluster].append(f"{rule.id}: no passport field models this point")
        elif absent:
            missing[rule.cluster].append(f"{rule.id}: {', '.join(absent)}")

        if rule.dynamic:
            dynamic.append(_freshness(payload, rule))

    coverage = [
        ClusterCoverage(
            cluster=cluster,
            required=len(ruleset.by_cluster(cluster)),
            present=len(ruleset.by_cluster(cluster)) - len(missing[cluster]),
            missing=missing[cluster],
        )
        for cluster in ruleset.clusters
    ]
    return ConformanceReport(
        ruleset_version=ruleset.version,
        ruleset_sha256=ruleset.sha256,
        clusters=ruleset.clusters,
        coverage=coverage,
        dynamic_fields=dynamic,
        checked_at=now,
    )


def _present(node: object, segments: list[str]) -> bool:
    """Whether the path leads to a non-empty value. A list needs only one item that does."""
    if isinstance(node, list):
        return any(_present(item, segments) for item in node)
    if not segments:
        return node not in (None, "", {}) and node != []
    if isinstance(node, dict):
        return _present(node.get(segments[0]), segments[1:])
    return False


def _reach(node: object, segments: list[str]) -> Iterator[object]:
    """Every value the path addresses, fanning out through lists."""
    if isinstance(node, list):
        for item in node:
            yield from _reach(item, segments)
    elif not segments:
        yield node
    elif isinstance(node, dict) and segments[0] in node:
        yield from _reach(node[segments[0]], segments[1:])


def _timestamps(node: object) -> Iterator[datetime]:
    if isinstance(node, datetime):
        # shortcut: a naive timestamp is read as UTC; require offsets once a producer sends local.
        yield node if node.tzinfo else node.replace(tzinfo=UTC)
    elif isinstance(node, dict):
        for value in node.values():
            yield from _timestamps(value)
    elif isinstance(node, list):
        for value in node:
            yield from _timestamps(value)


def _freshness(payload: object, rule: Rule) -> DynamicFieldState:
    """The oldest timestamp under the rule's paths. None found means unknown, hence stale."""
    found = [
        stamp
        for path in rule.paths
        for value in _reach(payload, path.split("."))
        for stamp in _timestamps(value)
    ]
    assert rule.max_age_days is not None  # the loader refuses a dynamic rule without one
    return DynamicFieldState(
        attribute=rule.id,
        last_refreshed_at=min(found) if found else None,
        max_age_days=rule.max_age_days,
    )
