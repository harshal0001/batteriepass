"""Path resolution against the schema, not against a payload.

Resolving against a payload only proves a path works for the documents that happen to
carry that field. Resolving against the schema proves the mapping is sound for every
document, including the ones where the field is absent — which is exactly the case
the conformance engine has to judge.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, Field

from bpass.bindings.battery_pass import BatteryPass
from bpass.conform import PathError, exists, resolve, unresolvable


class Inner(BaseModel):
    value: str = Field(alias="val")


class Middle(BaseModel):
    inner: Inner = Field(alias="in")
    optional_inner: Inner | None = Field(alias="opt", default=None)
    many: list[Inner] = Field(alias="list")
    scalar: int = Field(alias="num")


class Outer(BaseModel):
    middle: Middle = Field(alias="mid")


class TestResolution:
    def test_a_nested_path_resolves_to_its_type(self) -> None:
        assert resolve(Outer, "mid.in.val") is str

    def test_paths_use_payload_names_not_field_names(self) -> None:
        # Rule data sits next to regulation text and uses the keys that appear in
        # JSON. Python field names would leak the generator's mangling into the rules.
        assert exists(Outer, "mid.in.val")
        assert not exists(Outer, "middle.inner.value")

    def test_an_optional_field_is_traversed(self) -> None:
        # Optionality is the conformance engine's business. A rule may name a path
        # through a field that is frequently absent; that is the point.
        assert resolve(Outer, "mid.opt.val") is str

    def test_a_list_is_traversed_to_its_element(self) -> None:
        assert resolve(Outer, "mid.list.val") is str

    def test_the_root_itself_resolves(self) -> None:
        assert resolve(Outer, "mid") is Middle


class TestFailures:
    def test_an_unknown_segment_names_the_segment_and_the_alternatives(self) -> None:
        # "the path is wrong" is not actionable; naming the segment and what was
        # available turns a rule set bug into a one-line fix.
        with pytest.raises(PathError, match="no field 'nope'") as error:
            resolve(Outer, "mid.nope")
        assert "num" in str(error.value)

    def test_walking_through_a_scalar_says_so(self) -> None:
        with pytest.raises(PathError, match="is a scalar"):
            resolve(Outer, "mid.num.deeper")

    def test_an_empty_path_is_refused(self) -> None:
        with pytest.raises(PathError, match="empty path"):
            resolve(Outer, "")

    def test_unresolvable_reports_every_problem_not_just_the_first(self) -> None:
        problems = unresolvable(Outer, ("mid.in.val", "mid.nope", "mid.num.deeper"))
        assert len(problems) == 2


class TestAgainstTheRealBindings:
    @pytest.mark.parametrize(
        "path",
        [
            "performance.rated.capacity",
            "performance.dynamic.capacity.fade",
            "sustainability.carbonFootprint",
            "materials.composition.recycled",
            "conformity.declarationOfConformity",
            "safety.dismantling",
        ],
    )
    def test_representative_rule_paths_resolve(self, path: str) -> None:
        assert exists(BatteryPass, path)

    def test_a_plausible_but_wrong_path_does_not_resolve(self) -> None:
        # Guards against a resolver so permissive it would accept anything, which
        # would make the coverage check above meaningless.
        assert not exists(BatteryPass, "performance.rated.stateOfHealth")
