"""The rule set has to be trustworthy before anything can be judged against it.

Two independent claims are tested here, and they fail for different reasons.

The rule set is **faithful to the regulation**: every mandatory point is present, its
text matches the pinned source, and an amendment upstream is detected rather than
absorbed.

The rule set is **wired to the bindings**: every path it names exists in the aspect
model. This is the claim most likely to rot, because the aspect model is versioned
upstream and a path that resolved in BatteryPass 6.1.0 may resolve to nothing in the
next release — silently turning a mandatory attribute into one that can never be
present.
"""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path

import pytest

from bpass.bindings.battery_pass import BatteryPass
from bpass.conform import (
    Ruleset,
    RulesetError,
    available_versions,
    latest,
    load,
    text_digest,
    unresolvable,
)
from bpass.conform.ruleset import DEFAULT_ROOT
from bpass.core import ANNEX_XIII_CLUSTERS

# Counted from the pinned annex text, not from the loader that is under test.
EXPECTED_POINTS = {1: 19, 2: 4, 3: 1, 4: 4}
EXPECTED_TOTAL = sum(EXPECTED_POINTS.values())


@pytest.fixture(scope="module")
def ruleset() -> Ruleset:
    return latest()


@pytest.fixture
def ruleset_tree(tmp_path: Path) -> Path:
    root = tmp_path / "annex-xiii"
    shutil.copytree(DEFAULT_ROOT, root)
    load.cache_clear()
    yield root
    load.cache_clear()


class TestCompleteness:
    def test_every_mandatory_point_is_present(self, ruleset: Ruleset) -> None:
        assert len(ruleset.rules) == EXPECTED_TOTAL

    def test_each_part_has_the_points_the_regulation_gives_it(self, ruleset: Ruleset) -> None:
        # Part 1 ends at (s), not (t). Part 3 has no lettered points at all — it is a
        # single dashed item. Both are easy to get wrong from memory.
        assert dict(Counter(rule.part for rule in ruleset.rules)) == EXPECTED_POINTS

    def test_part_one_runs_from_a_to_s(self, ruleset: Ruleset) -> None:
        points = sorted(rule.point for rule in ruleset.rules if rule.part == 1)
        assert points == [chr(c) for c in range(ord("a"), ord("s") + 1)]

    def test_every_cluster_has_at_least_one_rule(self, ruleset: Ruleset) -> None:
        # A cluster with no rules would report as vacuously complete on every passport.
        for cluster in ANNEX_XIII_CLUSTERS:
            assert ruleset.by_cluster(cluster), f"{cluster} has no rules"

    def test_an_unmapped_point_is_reported_not_dropped(self, ruleset: Ruleset) -> None:
        """Point 2(b) has no equivalent in BatteryPass 6.1.0.

        It asks for part numbers for components and contact details for replacement
        spares. Dropping it would overstate conformance by one attribute; keeping it
        unmapped makes the gap visible in the coverage report.
        """
        unmapped = [rule.id for rule in ruleset.unmapped_rules]
        assert unmapped == ["XIII.2.b"]
        assert ruleset.rules[0].mapped


class TestAccessLevels:
    def test_access_levels_come_from_the_part_headings(self, ruleset: Ruleset) -> None:
        by_part = {rule.part: rule.access for rule in ruleset.rules}
        assert by_part[1] == "public"
        assert by_part[2] == "legitimate_interest"
        assert by_part[3] == "notified_bodies"
        assert by_part[4] == "legitimate_interest"

    def test_only_part_four_describes_an_individual_battery(self, ruleset: Ruleset) -> None:
        for rule in ruleset.rules:
            expected = "individual" if rule.part == 4 else "model"
            assert rule.scope == expected


class TestDynamicFields:
    def test_dynamic_fields_are_exactly_the_individual_battery_points(
        self, ruleset: Ruleset
    ) -> None:
        # The alignment is the regulation's, not ours: information about an individual
        # battery is what changes over its life.
        assert {rule.id for rule in ruleset.dynamic_rules} == {
            "XIII.4.a",
            "XIII.4.b",
            "XIII.4.c",
            "XIII.4.d",
        }

    def test_state_of_health_is_dynamic_and_mapped(self, ruleset: Ruleset) -> None:
        """The point the model exists to satisfy.

        State of health cannot be measured directly. If this rule is ever unmapped or
        marked static, the passport stops requiring the one number this project
        estimates, and the project has no reason to contain a model.
        """
        rule = next(r for r in ruleset.rules if r.id == "XIII.4.b")
        assert rule.dynamic
        assert rule.mapped
        assert "state of health" in rule.text.lower()

    def test_every_dynamic_rule_declares_a_refresh_interval(self, ruleset: Ruleset) -> None:
        for rule in ruleset.dynamic_rules:
            assert rule.max_age_days and rule.max_age_days > 0

    def test_static_rules_declare_no_refresh_interval(self, ruleset: Ruleset) -> None:
        for rule in ruleset.rules:
            if not rule.dynamic:
                assert rule.max_age_days is None


class TestPathsResolveAgainstTheBindings:
    def test_every_mapped_path_exists_in_the_aspect_model(self, ruleset: Ruleset) -> None:
        problems = unresolvable(BatteryPass, ruleset.paths)
        assert problems == [], "\n".join(problems)

    def test_the_ruleset_maps_a_meaningful_number_of_paths(self, ruleset: Ruleset) -> None:
        # A guard against a mapping that silently empties out. If a regeneration drops
        # most paths, coverage would read as "nothing required" rather than as broken.
        assert len(ruleset.paths) > 30


class TestTamperDetection:
    def test_amended_regulation_text_un_reviews_its_rule(self, ruleset_tree: Path) -> None:
        """The whole point of carrying a digest.

        Text edited upstream must not be absorbed silently: the mapping was made
        against the old wording and has to be looked at again.
        """
        path = ruleset_tree / "2025-07-31" / "ruleset.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["rules"][0]["text"] = "something the regulation does not say"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _rehash(ruleset_tree / "2025-07-31")

        with pytest.raises(RulesetError, match="does not match its recorded digest"):
            load("2025-07-31", ruleset_tree)

    def test_a_modified_ruleset_file_is_refused(self, ruleset_tree: Path) -> None:
        path = ruleset_tree / "2025-07-31" / "ruleset.json"
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        with pytest.raises(RulesetError, match="hash mismatch"):
            load("2025-07-31", ruleset_tree)

    def test_a_modified_regulation_text_is_refused(self, ruleset_tree: Path) -> None:
        path = ruleset_tree / "2025-07-31" / "annex-xiii.txt"
        path.write_text(path.read_text(encoding="utf-8") + "\n(t) invented\n", encoding="utf-8")
        with pytest.raises(RulesetError, match="hash mismatch"):
            load("2025-07-31", ruleset_tree)

    def test_an_unknown_version_names_what_is_available(self, ruleset_tree: Path) -> None:
        with pytest.raises(RulesetError, match="2025-07-31"):
            load("1999-01-01", ruleset_tree)


class TestDigest:
    def test_reflowed_whitespace_is_not_an_amendment(self) -> None:
        # EUR-Lex markup reflows between publications. That is not a legal change.
        assert text_digest("rated capacity  (in Ah);") == text_digest("rated capacity (in Ah);")

    def test_a_real_wording_change_is_an_amendment(self) -> None:
        assert text_digest("rated capacity (in Ah);") != text_digest("rated capacity (in Wh);")


class TestVersioning:
    def test_versions_are_served_side_by_side(self) -> None:
        versions = available_versions()
        assert versions
        assert all(load(version).version == version for version in versions)

    def test_latest_is_the_newest_by_date(self) -> None:
        assert latest().version == available_versions()[-1]

    def test_the_ruleset_carries_its_own_hash(self, ruleset: Ruleset) -> None:
        # Stamped on every conformance report, so a stored passport can always say
        # which reading of the rules judged it.
        assert len(ruleset.sha256) == 64


def _rehash(directory: Path) -> None:
    """Rewrite the manifest so a hash check passes and the digest check is reached."""
    import hashlib

    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative in manifest["files"]:
        manifest["files"][relative] = hashlib.sha256(
            (directory / relative).read_bytes()
        ).hexdigest()
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
