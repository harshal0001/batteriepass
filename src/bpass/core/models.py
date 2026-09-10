"""Domain models.

Three ideas drive the shapes here.

1. **Coverage, not a verdict.** Annex XIII splits the passport into seven clusters.
   A single ``conformant: bool`` tells a manufacturer nothing about what to fix, so
   every check reports per-cluster counts and names every missing attribute.
2. **Provenance on every record.** Both the regulation and the model will change.
   A stored passport that cannot say which model version and which reading of the
   rules produced it is not auditable, and auditability is the entire point.
3. **An estimate is not a measurement.** State of health cannot be read off a cell.
   Annex XIII still requires the number, so the number ships with a calibrated
   interval and an explicit statement that it is not certified.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Cluster(StrEnum):
    """The seven Annex XIII data clusters.

    Names follow the regulation's own grouping, not an internal taxonomy, so a
    coverage report can be read against the legal text side by side.
    """

    GENERAL = "general"
    COMPLIANCE = "compliance"
    CARBON_FOOTPRINT = "carbon_footprint"
    DUE_DILIGENCE = "due_diligence"
    MATERIALS = "materials"
    CIRCULARITY = "circularity"
    PERFORMANCE_DURABILITY = "performance_durability"


ANNEX_XIII_CLUSTERS: tuple[Cluster, ...] = tuple(Cluster)
"""All seven clusters, in report order. A coverage report must cover every one of
them, including the clusters that scored zero — an omitted cluster reads as a pass."""


class ClusterCoverage(BaseModel):
    """How complete one cluster is.

    ``missing`` names attributes individually. A count alone would let a report say
    "4 of 9 present" without ever telling anyone which five to go and collect.
    """

    model_config = ConfigDict(frozen=True)

    cluster: Cluster
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


class SoHEstimate(BaseModel):
    """A state-of-health estimate and everything needed to reproduce it.

    ``model_sha256`` is the hash of the served ONNX file, not of the training run.
    It answers "which bytes produced this number", which is the question an auditor
    asks and the one a training-run id cannot answer.
    """

    # Pydantic reserves the ``model_`` prefix for its own API. These field names come
    # from the passport's provenance vocabulary and are not negotiable, so the
    # namespace guard is switched off here deliberately.
    model_config = ConfigDict(frozen=True, protected_namespaces=())

    soh_percent: float = Field(
        ge=0.0,
        le=120.0,
        description="Remaining capacity as a percentage of rated capacity. Values "
        "slightly above 100 are physical, not errors: cells often gain capacity "
        "over the first few dozen cycles.",
    )
    soh_interval: PredictionInterval | None = None
    rul_cycles: int | None = Field(default=None, ge=0)
    rul_interval: PredictionInterval | None = None

    model_version: str = Field(min_length=1, examples=["cnn1d-v3"])
    model_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    observed_cycles: int = Field(gt=0, description="Cycles the prediction window used.")
    predicted_at: datetime

    certified: Literal[False] = False
    """Never true. Present so that any consumer reading the JSON sees the claim
    denied explicitly rather than having to know it was never made."""


class DynamicFieldState(BaseModel):
    """Freshness of one dynamic Annex XIII attribute.

    Annex XIII distinguishes static fields from dynamic ones that must be updated
    through the battery's life. A passport whose state of health was computed once
    at manufacture and never again satisfies the schema and defeats the regulation.
    Staleness is therefore a first-class part of the report, not a footnote.
    """

    model_config = ConfigDict(frozen=True)

    attribute: str = Field(min_length=1)
    last_refreshed_at: datetime
    max_age_days: int = Field(gt=0, description="Refresh interval this attribute expects.")

    def stale_at(self, now: datetime) -> bool:
        return (now - self.last_refreshed_at).days > self.max_age_days


class ConformanceReport(BaseModel):
    """The result of checking one passport against one version of the rule set."""

    model_config = ConfigDict(frozen=True)

    ruleset_version: str = Field(min_length=1, examples=["annex-xiii-2026-07"])
    ruleset_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coverage: list[ClusterCoverage]
    dynamic_fields: list[DynamicFieldState] = Field(default_factory=list)
    checked_at: datetime

    @model_validator(mode="after")
    def _every_cluster_reported(self) -> Self:
        seen = [c.cluster for c in self.coverage]
        if len(seen) != len(set(seen)):
            raise ValueError("a cluster is reported twice")
        if set(seen) != set(ANNEX_XIII_CLUSTERS):
            absent = sorted(set(ANNEX_XIII_CLUSTERS) - set(seen))
            raise ValueError(f"coverage omits clusters: {', '.join(absent)}")
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
    """A stored passport: the document, the estimate that filled its dynamic fields,
    and the conformance verdict that was true when it was written.

    Generic over the passport type so that ``core`` stays independent of
    ``bindings``, which is generated from the SAMM aspect model and regenerated
    whenever Catena-X publishes a new version. In the running service ``PassportT``
    is the generated ``BatteryPass``.
    """

    model_config = ConfigDict(frozen=True)

    id: str = Field(min_length=1, description="DynamoDB partition key.")
    passport: PassportT
    soh: SoHEstimate
    conformance: ConformanceReport
    is_demo: bool = Field(
        default=False,
        description="Seeded records backing the public QR links. The store refuses to "
        "overwrite or delete these.",
    )
    created_at: datetime
