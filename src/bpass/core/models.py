"""Domain models.

Three ideas drive the shapes here.

1. **Coverage, not a verdict.** Every rule set groups its rules into clusters — seven
   for Annex XIII. A single ``conformant: bool`` tells a manufacturer nothing about
   what to fix, so every check reports per-cluster counts and names every missing
   attribute.
2. **Provenance on every record.** The rules, the model and the source documents will
   all change. A stored passport that cannot say which model, which reading of the
   rules and which page of which document produced it is not auditable, and
   auditability is the entire point.
3. **An estimate is not a measurement.** State of health and remaining useful life
   cannot be read off an asset. The number ships with a calibrated interval, a drift
   flag and an explicit statement that it is not certified.

Nothing here knows which asset it describes. Asset specifics — the clusters, the
passport schema, the model — come from the profile's data. See docs/adr/0003.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Profile(StrEnum):
    """The asset profiles. Each is a folder of data under ``profiles/``."""

    BATTERY = "battery"
    ENGINE = "engine"


class ClusterCoverage(BaseModel):
    """How complete one cluster is.

    ``missing`` names attributes individually. A count alone would let a report say
    "4 of 9 present" without ever telling anyone which five to go and collect.
    """

    model_config = ConfigDict(frozen=True)

    cluster: str = Field(min_length=1, description="As declared by the rule set.")
    required: int = Field(ge=0, description="Mandatory attributes in this cluster.")
    present: int = Field(ge=0, description="Mandatory attributes actually supplied.")
    missing: list[str] = Field(
        default_factory=list,
        description="Semantic names of the mandatory attributes that are absent.",
    )

    @model_validator(mode="after")
    def _counts_agree(self) -> Self:
        if self.present > self.required:
            raise ValueError(
                f"{self.cluster}: present ({self.present}) exceeds required ({self.required})"
            )
        if len(self.missing) != self.required - self.present:
            raise ValueError(
                f"{self.cluster}: {len(self.missing)} attributes named as missing but "
                f"{self.required - self.present} are unaccounted for"
            )
        return self

    @property
    def complete(self) -> bool:
        return self.present == self.required


class PredictionInterval(BaseModel):
    """A distribution-free interval around a point estimate.

    Split conformal prediction, calibrated on held-out cells. ``nominal_coverage`` is
    what was asked for; ``empirical_coverage`` is what the calibration set actually
    delivered. Publishing both is the honest form — a nominal 90% band that covers
    71% of held-out cells is worse than no band at all, and only the second number
    reveals it.
    """

    model_config = ConfigDict(frozen=True)

    lower: float
    upper: float
    nominal_coverage: float = Field(gt=0.0, lt=1.0, description="e.g. 0.90")
    empirical_coverage: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Measured on the calibration split. None until calibration has run.",
    )
    method: Literal["split-conformal"] = "split-conformal"

    @model_validator(mode="after")
    def _ordered(self) -> Self:
        if self.lower > self.upper:
            raise ValueError(f"interval is inverted: [{self.lower}, {self.upper}]")
        return self


class HealthEstimate(BaseModel):
    """One health estimate and everything needed to reproduce it.

    ``model_sha256`` is the hash of the served ONNX file, not of the training run.
    It answers "which bytes produced this number", which is the question an auditor
    asks and the one a training-run id cannot answer.
    """

    # Pydantic reserves the ``model_`` prefix for its own API. These field names come
    # from the passport's provenance vocabulary and are not negotiable, so the
    # namespace guard is switched off here deliberately.
    model_config = ConfigDict(frozen=True, protected_namespaces=())

    target: Literal["soh_percent", "rul_cycles"]
    value: float = Field(
        ge=0.0,
        description="State of health may sit slightly above 100: cells often gain "
        "capacity over the first few dozen cycles. That is physical, not an error.",
    )
    interval: PredictionInterval | None = Field(
        default=None, description="None until the model has been conformally calibrated."
    )
    in_distribution: bool | None = Field(
        default=None,
        description="False when the inputs drift from the training data, and the estimate "
        "is shown as unreliable. None until the model ships a drift reference.",
    )
    drift_features: list[str] = Field(
        default_factory=list, description="The inputs that triggered the drift flag."
    )

    model_version: str = Field(min_length=1, examples=["cnn1d-v3"])
    model_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    observed_window: int = Field(gt=0, description="Cycles the prediction window used.")
    predicted_at: datetime

    certified: Literal[False] = False
    """Never true. Present so that any consumer reading the JSON sees the claim
    denied explicitly rather than having to know it was never made."""

    @model_validator(mode="after")
    def _plausible(self) -> Self:
        if self.target == "soh_percent" and self.value > 120.0:
            raise ValueError(f"state of health {self.value}% is not physical")
        if self.drift_features and self.in_distribution is not False:
            raise ValueError("drift features are listed but the estimate is not flagged")
        return self


class FieldProvenance(BaseModel):
    """Where one extracted passport value came from.

    A value without a page and a verbatim quote cannot be checked against its source,
    so extraction drops any value that lacks them. See docs/adr/0006.
    """

    model_config = ConfigDict(frozen=True)

    field: str = Field(min_length=1, description="Passport field path.")
    value: str
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$", description="Of the source PDF.")
    page: int = Field(ge=1)
    quote: str = Field(min_length=1, description="Verbatim text the value came from.")
    method: Literal["llm", "manual"]
    verified: bool = Field(
        description="The quote was found on that page and the value agrees with it."
    )


class DynamicFieldState(BaseModel):
    """Freshness of one dynamic Annex XIII attribute.

    Annex XIII distinguishes static fields from dynamic ones that must be updated
    through the battery's life. A passport whose state of health was computed once
    at manufacture and never again satisfies the schema and defeats the regulation.
    Staleness is therefore a first-class part of the report, not a footnote.
    """

    model_config = ConfigDict(frozen=True)

    attribute: str = Field(min_length=1)
    last_refreshed_at: datetime | None = Field(
        description="None when the passport carries no timestamp for this field."
    )
    max_age_days: int = Field(gt=0, description="Refresh interval this attribute expects.")

    def stale_at(self, now: datetime) -> bool:
        # Unknown counts as stale: nothing proves the value was ever refreshed.
        if self.last_refreshed_at is None:
            return True
        return (now - self.last_refreshed_at).days > self.max_age_days


class ConformanceReport(BaseModel):
    """The result of checking one passport against one version of the rule set."""

    model_config = ConfigDict(frozen=True)

    ruleset_version: str = Field(min_length=1, examples=["annex-xiii-2026-07"])
    ruleset_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    clusters: tuple[str, ...] = Field(
        min_length=1, description="Every cluster the rule set declares, in report order."
    )
    coverage: list[ClusterCoverage]
    dynamic_fields: list[DynamicFieldState] = Field(default_factory=list)
    checked_at: datetime

    @model_validator(mode="after")
    def _every_cluster_reported(self) -> Self:
        seen = [c.cluster for c in self.coverage]
        if len(seen) != len(set(seen)):
            raise ValueError("a cluster is reported twice")
        # An omitted cluster reads as a pass, so every declared cluster must appear,
        # including the ones that scored zero.
        if set(seen) != set(self.clusters):
            absent = sorted(set(self.clusters) - set(seen))
            unknown = sorted(set(seen) - set(self.clusters))
            if absent:
                raise ValueError(f"coverage omits clusters: {', '.join(absent)}")
            raise ValueError(f"coverage reports undeclared clusters: {', '.join(unknown)}")
        return self

    @property
    def conformant(self) -> bool:
        """True only when every mandatory attribute in every cluster is present."""
        return all(c.complete for c in self.coverage)

    @property
    def required(self) -> int:
        return sum(c.required for c in self.coverage)

    @property
    def present(self) -> int:
        return sum(c.present for c in self.coverage)

    def stale_fields(self, now: datetime | None = None) -> list[DynamicFieldState]:
        moment = now if now is not None else datetime.now(UTC)
        return [f for f in self.dynamic_fields if f.stale_at(moment)]


class PassportRecord[PassportT: BaseModel](BaseModel):
    """A stored passport: the document, the estimates that filled its dynamic fields,
    where its extracted values came from, and the conformance verdict that was true
    when it was written.

    Generic over the passport type so that ``core`` stays independent of
    ``bindings``, which is generated from the SAMM aspect model and regenerated
    whenever Catena-X publishes a new version. In the running service ``PassportT``
    is the profile's generated passport model, such as ``BatteryPass``.
    """

    model_config = ConfigDict(frozen=True)

    id: str = Field(min_length=1, description="DynamoDB partition key.")
    profile: Profile
    passport: PassportT
    health: list[HealthEstimate] = Field(
        min_length=1, description="One per target: a battery carries both SoH and RUL."
    )
    conformance: ConformanceReport
    provenance: list[FieldProvenance] = Field(default_factory=list)
    is_demo: bool = Field(
        default=False,
        description="Seeded records backing the public QR links. The store refuses to "
        "overwrite or delete these.",
    )
    created_at: datetime

    @model_validator(mode="after")
    def _one_estimate_per_target(self) -> Self:
        targets = [h.target for h in self.health]
        if len(targets) != len(set(targets)):
            raise ValueError("more than one health estimate for the same target")
        return self
