"""The domain contract has to reject records that would be misleading if stored.

These are not schema tests. Pydantic already checks types. What is checked here is
the small set of invariants that make a stored passport auditable: a coverage report
that silently omits a cluster reads as a pass, a missing-attribute list that does not
add up hides work from whoever has to fix it, and an inverted interval is nonsense
that would render as a plausible-looking band.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import BaseModel, ValidationError

from bpass.core import (
    ClusterCoverage,
    ConformanceReport,
    DynamicFieldState,
    FieldProvenance,
    HealthEstimate,
    PassportRecord,
    PredictionInterval,
    Profile,
)

SHA = "a" * 64
NOW = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)
CLUSTERS = ("general", "materials", "carbon_footprint")


def full_coverage(missing_from: str | None = None) -> list[ClusterCoverage]:
    """A report covering every declared cluster, optionally with one gap."""
    out = []
    for cluster in CLUSTERS:
        if cluster == missing_from:
            out.append(
                ClusterCoverage(cluster=cluster, required=3, present=2, missing=["carbonFootprint"])
            )
        else:
            out.append(ClusterCoverage(cluster=cluster, required=3, present=3))
    return out


class TestClusterCoverage:
    def test_missing_list_must_account_for_every_gap(self) -> None:
        # Two attributes absent but only one named: the report would understate the work.
        with pytest.raises(ValidationError, match="unaccounted for"):
            ClusterCoverage(cluster="materials", required=5, present=3, missing=["a"])

    def test_present_cannot_exceed_required(self) -> None:
        with pytest.raises(ValidationError, match="exceeds required"):
            ClusterCoverage(cluster="general", required=2, present=3, missing=[])

    def test_complete_when_nothing_missing(self) -> None:
        assert ClusterCoverage(cluster="general", required=4, present=4).complete

    def test_an_empty_cluster_is_complete(self) -> None:
        # A cluster with no mandatory attributes is vacuously satisfied. It must still
        # appear in the report so a reader can see it was considered.
        assert ClusterCoverage(cluster="due_diligence", required=0, present=0).complete


class TestDynamicFieldState:
    def test_no_timestamp_counts_as_stale(self) -> None:
        # Nothing proves the value was ever refreshed.
        field = DynamicFieldState(attribute="XIII.4.c", last_refreshed_at=None, max_age_days=365)
        assert field.stale_at(NOW)


class TestConformanceReport:
    def test_omitting_a_cluster_is_rejected(self) -> None:
        partial = full_coverage()[:-1]
        with pytest.raises(ValidationError, match="omits clusters"):
            ConformanceReport(
                ruleset_version="annex-xiii-2026-07",
                ruleset_sha256=SHA,
                clusters=CLUSTERS,
                coverage=partial,
                checked_at=NOW,
            )

    def test_a_cluster_the_rule_set_does_not_declare_is_rejected(self) -> None:
        extra = [*full_coverage(), ClusterCoverage(cluster="invented", required=1, present=1)]
        with pytest.raises(ValidationError, match="undeclared clusters"):
            ConformanceReport(
                ruleset_version="annex-xiii-2026-07",
                ruleset_sha256=SHA,
                clusters=CLUSTERS,
                coverage=extra,
                checked_at=NOW,
            )

    def test_duplicate_cluster_is_rejected(self) -> None:
        doubled = [*full_coverage(), full_coverage()[0]]
        with pytest.raises(ValidationError, match="reported twice"):
            ConformanceReport(
                ruleset_version="annex-xiii-2026-07",
                ruleset_sha256=SHA,
                clusters=CLUSTERS,
                coverage=doubled,
                checked_at=NOW,
            )

    def test_conformant_only_when_every_cluster_is_complete(self) -> None:
        report = ConformanceReport(
            ruleset_version="annex-xiii-2026-07",
            ruleset_sha256=SHA,
            clusters=CLUSTERS,
            coverage=full_coverage(),
            checked_at=NOW,
        )
        assert report.conformant
        assert report.required == report.present == 9

        gapped = report.model_copy(
            update={"coverage": full_coverage(missing_from="carbon_footprint")}
        )
        assert not gapped.conformant
        assert gapped.present == 8

    def test_stale_dynamic_fields_are_reported(self) -> None:
        report = ConformanceReport(
            ruleset_version="annex-xiii-2026-07",
            ruleset_sha256=SHA,
            clusters=CLUSTERS,
            coverage=full_coverage(),
            dynamic_fields=[
                DynamicFieldState(
                    attribute="stateOfHealth",
                    last_refreshed_at=NOW - timedelta(days=400),
                    max_age_days=365,
                ),
                DynamicFieldState(
                    attribute="cycleCount",
                    last_refreshed_at=NOW - timedelta(days=10),
                    max_age_days=365,
                ),
            ],
            checked_at=NOW,
        )
        # A conformant passport can still be stale. The two verdicts are independent,
        # which is the whole reason freshness is modelled separately.
        assert report.conformant
        assert [f.attribute for f in report.stale_fields(NOW)] == ["stateOfHealth"]


def estimate(**overrides: object) -> HealthEstimate:
    fields: dict[str, object] = {
        "target": "soh_percent",
        "value": 88.2,
        "model_version": "cnn1d-v3",
        "model_sha256": SHA,
        "observed_window": 100,
        "predicted_at": NOW,
    }
    return HealthEstimate.model_validate(fields | overrides)


class TestHealthEstimate:
    def test_capacity_above_100_percent_is_allowed(self) -> None:
        # Cells commonly gain a little capacity over their first cycles. Clamping at
        # 100 would silently rewrite a real measurement.
        assert estimate(value=101.4).value == pytest.approx(101.4)

    def test_implausible_state_of_health_is_rejected(self) -> None:
        with pytest.raises(ValidationError, match="not physical"):
            estimate(value=150.0)

    def test_remaining_useful_life_is_not_capped_like_a_percentage(self) -> None:
        assert estimate(target="rul_cycles", value=180.0).value == 180.0

    def test_model_hash_must_be_a_sha256(self) -> None:
        with pytest.raises(ValidationError):
            estimate(model_sha256="not-a-hash")

    def test_certified_cannot_be_set_true(self) -> None:
        with pytest.raises(ValidationError):
            estimate(certified=True)

    def test_drift_features_require_the_unreliable_flag(self) -> None:
        # Listing the drifting inputs while still presenting the estimate as reliable
        # would hide the warning the features exist to give.
        with pytest.raises(ValidationError, match="not flagged"):
            estimate(drift_features=["voltage_variance"])
        flagged = estimate(in_distribution=False, drift_features=["voltage_variance"])
        assert flagged.drift_features == ["voltage_variance"]

    def test_provenance_fields_survive_serialisation(self) -> None:
        # Pydantic reserves the model_ prefix; if the namespace guard were left on,
        # these would be renamed or warned away and provenance would leave the record.
        dumped = estimate().model_dump()
        assert dumped["model_version"] == "cnn1d-v3"
        assert dumped["model_sha256"] == SHA
        assert dumped["certified"] is False


class TestFieldProvenance:
    def test_pages_are_counted_from_one(self) -> None:
        with pytest.raises(ValidationError):
            FieldProvenance(
                field="manufacturer",
                value="A123",
                source_sha256=SHA,
                page=0,
                quote="Manufacturer: A123",
                method="llm",
                verified=True,
            )


class TestPredictionInterval:
    def test_inverted_interval_is_rejected(self) -> None:
        with pytest.raises(ValidationError, match="inverted"):
            PredictionInterval(lower=92.0, upper=88.0, nominal_coverage=0.9)

    def test_empirical_coverage_is_optional_until_calibrated(self) -> None:
        assert (
            PredictionInterval(lower=88.0, upper=92.0, nominal_coverage=0.9).empirical_coverage
            is None
        )


class DummyPassport(BaseModel):
    """Stands in for a profile's generated passport model."""

    manufacturer: str


class TestPassportRecord:
    def test_record_is_generic_over_the_generated_passport_type(self) -> None:
        record = PassportRecord[DummyPassport](
            id="bp-0001",
            profile=Profile.BATTERY,
            passport=DummyPassport(manufacturer="A123"),
            health=[estimate(), estimate(target="rul_cycles", value=640.0)],
            conformance=ConformanceReport(
                ruleset_version="annex-xiii-2026-07",
                ruleset_sha256=SHA,
                clusters=CLUSTERS,
                coverage=full_coverage(),
                checked_at=NOW,
            ),
            created_at=NOW,
        )
        assert record.passport.manufacturer == "A123"
        assert record.is_demo is False
        # Round-trips: what goes into DynamoDB comes back the same shape.
        assert PassportRecord[DummyPassport].model_validate(record.model_dump()) == record

    def test_one_estimate_per_target(self) -> None:
        with pytest.raises(ValidationError, match="same target"):
            PassportRecord[DummyPassport](
                id="bp-0002",
                profile=Profile.BATTERY,
                passport=DummyPassport(manufacturer="A123"),
                health=[estimate(), estimate(value=80.0)],
                conformance=ConformanceReport(
                    ruleset_version="annex-xiii-2026-07",
                    ruleset_sha256=SHA,
                    clusters=CLUSTERS,
                    coverage=full_coverage(),
                    checked_at=NOW,
                ),
                created_at=NOW,
            )
