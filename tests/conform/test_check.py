"""The checker decides what "conformant" means, so each presence rule is pinned here.

Every test starts from the official BatteryPass 6.1.0 example payload and changes one
thing, so a failure points at one rule rather than at a fixture.
"""

from __future__ import annotations

import copy
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel

from bpass.bindings.battery_pass import BatteryPass
from bpass.conform import Rule, Ruleset, check, latest
from bpass.core import ConformanceReport

EXAMPLE = (
    Path(__file__).resolve().parents[2]
    / "profiles/battery/samm-models/io.catenax.battery.battery_pass/6.1.0/gen/BatteryPass.json"
)
NOW = datetime(2026, 10, 26, tzinfo=UTC)


@pytest.fixture(scope="module")
def ruleset() -> Ruleset:
    return latest()


@pytest.fixture
def payload() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    return copy.deepcopy(data)


def run(payload: dict[str, Any], ruleset: Ruleset) -> ConformanceReport:
    return check(BatteryPass.model_validate(payload), ruleset, NOW)


def missing(report: ConformanceReport, cluster: str) -> list[str]:
    return next(c.missing for c in report.coverage if c.cluster == cluster)


class TestPresence:
    def test_the_official_example_lacks_only_the_unmapped_point(
        self, payload: dict[str, Any], ruleset: Ruleset
    ) -> None:
        report = run(payload, ruleset)
        assert (report.present, report.required) == (27, 28)
        assert missing(report, "materials") == ["XIII.2.b: no passport field models this point"]
        assert not report.conformant

    def test_every_declared_cluster_is_reported_in_order(
        self, payload: dict[str, Any], ruleset: Ruleset
    ) -> None:
        assert tuple(c.cluster for c in run(payload, ruleset).coverage) == ruleset.clusters

    def test_a_multi_path_rule_needs_every_path(
        self, payload: dict[str, Any], ruleset: Ruleset
    ) -> None:
        # 4(d) names four fields; three of them do not make the point.
        payload["performance"]["dynamic"]["negativeEvents"] = []
        assert "XIII.4.d: performance.dynamic.negativeEvents" in missing(
            run(payload, ruleset), "performance_durability"
        )

    def test_an_empty_list_misses_every_path_through_it(
        self, payload: dict[str, Any], ruleset: Ruleset
    ) -> None:
        payload["materials"]["composition"] = []
        gaps = missing(run(payload, ruleset), "materials")
        assert "XIII.1.e: materials.composition.recycled" in gaps
        assert "XIII.1.f: materials.composition.renewable" in gaps
        assert any(g.startswith("XIII.1.b:") and "materials.composition" in g for g in gaps)

    def test_an_empty_string_is_absent(self, payload: dict[str, Any], ruleset: Ruleset) -> None:
        payload["identification"]["chemistry"] = ""
        assert "XIII.1.b: identification.chemistry" in missing(run(payload, ruleset), "materials")


class Part(BaseModel):
    share: float | None = None


class Product(BaseModel):
    parts: list[Part]


def one_rule(path: str) -> Ruleset:
    rule = Rule(
        id="T.1",
        part=1,
        point="a",
        text="",
        access="public",
        scope="model",
        cluster="general",
        paths=(path,),
        dynamic=False,
    )
    return Ruleset(version="test", sha256="0" * 64, clusters=("general",), rules=(rule,))


class TestPresenceRules:
    """The editorial rules themselves, on a minimal model where every case can occur."""

    def test_one_list_item_carrying_the_field_is_enough(self) -> None:
        product = Product(parts=[Part(), Part(share=0.4)])
        assert check(product, one_rule("parts.share"), NOW).conformant

    def test_no_list_item_carrying_it_is_missing(self) -> None:
        report = check(Product(parts=[Part(), Part()]), one_rule("parts.share"), NOW)
        assert report.coverage[0].missing == ["T.1: parts.share"]

    def test_zero_is_a_value(self) -> None:
        assert check(Product(parts=[Part(share=0.0)]), one_rule("parts.share"), NOW).conformant


class TestFreshness:
    def test_old_timestamps_are_stale(self, payload: dict[str, Any], ruleset: Ruleset) -> None:
        stale = {f.attribute for f in run(payload, ruleset).stale_fields(NOW)}
        assert stale == {"XIII.4.a", "XIII.4.b", "XIII.4.c", "XIII.4.d"}

    def test_recent_timestamps_are_fresh(self, payload: dict[str, Any], ruleset: Ruleset) -> None:
        text = json.dumps(payload).replace("2023-12-07T10:39:13.576", "2026-10-01T10:00:00")
        stale = {f.attribute for f in run(json.loads(text), ruleset).stale_fields(NOW)}
        # 4(c) is the battery's status, which carries no timestamp: unknown stays stale.
        assert stale == {"XIII.4.c"}

    def test_the_oldest_timestamp_under_a_rule_decides(
        self, payload: dict[str, Any], ruleset: Ruleset
    ) -> None:
        text = json.dumps(payload).replace("2023-12-07T10:39:13.576", "2026-10-01T10:00:00")
        fresh = json.loads(text)
        fresh["performance"]["dynamic"]["power"]["remaining"]["time"] = "2020-01-01T00:00:00Z"
        stale = {f.attribute for f in run(fresh, ruleset).stale_fields(NOW)}
        assert "XIII.4.a" in stale
