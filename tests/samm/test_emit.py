"""What the emitter has to get right about Python.

The name mangling is where property-based testing earns its place. Example-based tests
prove the cases someone thought of; the invariant that matters is that *every* SAMM
property name yields a valid, non-colliding Python identifier, and there are 246 of
them in this model with more arriving every upstream release.
"""

from __future__ import annotations

import keyword

import pytest
from hypothesis import given
from hypothesis import strategies as st

from bpass.samm.emit import (
    XSD_PREFIX,
    class_names,
    collapse,
    pascal_case,
    python_type,
    snake_case,
)
from bpass.samm.model import Characteristic, ResolvedModel, UnsupportedConstruct

# SAMM property names are NCNames in practice: letters, digits and underscores,
# starting with a letter. That is the input domain, so that is what is generated.
samm_names = st.from_regex(r"\A[A-Za-z][A-Za-z0-9_]{0,40}\Z", fullmatch=True)


class TestNameMangling:
    @given(samm_names)
    def test_every_samm_name_yields_a_valid_identifier(self, name: str) -> None:
        result = snake_case(name)
        assert result.isidentifier()
        assert not keyword.iskeyword(result)

    @given(samm_names)
    def test_snake_case_is_idempotent(self, name: str) -> None:
        once = snake_case(name)
        assert snake_case(once) == once

    @pytest.mark.parametrize(
        ("samm", "python"),
        [
            ("batteryCategory", "battery_category"),
            ("idDmc", "id_dmc"),
            ("stateOfCharge", "state_of_charge"),
            ("CO2FootprintTotal", "co2_footprint_total"),
            ("BPNL", "bpnl"),
            ("class", "class_"),
            ("import", "import_"),
            ("match", "match_"),
        ],
    )
    def test_known_names(self, samm: str, python: str) -> None:
        assert snake_case(samm) == python

    def test_a_name_that_cannot_become_an_identifier_raises(self) -> None:
        with pytest.raises(UnsupportedConstruct):
            snake_case("---")

    @pytest.mark.parametrize(
        ("samm", "python"),
        [("battery_pass", "BatteryPass"), ("BatteryPass", "BatteryPass"), ("uuid", "Uuid")],
    )
    def test_pascal_case(self, samm: str, python: str) -> None:
        assert pascal_case(samm) == python


class TestClassNames:
    def test_colliding_entity_names_are_qualified_by_namespace(self, model: ResolvedModel) -> None:
        """Two models define IdentificationEntity, two define KeyValueList.

        A generator keyed on the local name emits one class and binds both, which
        compiles and produces wrong data. The collision is real in this model, not
        hypothetical.
        """
        names = class_names(model)
        assert len(set(names.values())) == len(names)
        assert "BatteryPassIdentificationEntity" in names.values()
        assert "SerialPartKeyValueList" in names.values()

    def test_non_colliding_names_stay_readable(self, model: ResolvedModel) -> None:
        # Qualifying everything would be simpler and would make the bindings unreadable.
        assert "OperationEntity" in class_names(model).values()


class TestTypeMapping:
    @pytest.mark.parametrize(
        ("xsd", "python"),
        [
            ("string", "str"),
            ("double", "float"),
            ("float", "float"),
            ("integer", "int"),
            ("boolean", "bool"),
            ("dateTime", "datetime"),
            ("anyURI", "str"),
        ],
    )
    def test_scalars(self, xsd: str, python: str) -> None:
        characteristic = Characteristic(
            urn="urn:test#C", kind="Text", data_type=f"{XSD_PREFIX}{xsd}"
        )
        assert python_type(characteristic, {}) == python

    def test_an_unmapped_xsd_type_raises_rather_than_defaulting_to_str(self) -> None:
        characteristic = Characteristic(
            urn="urn:test#C", kind="Text", data_type=f"{XSD_PREFIX}gYearMonth"
        )
        with pytest.raises(UnsupportedConstruct, match="gYearMonth"):
            python_type(characteristic, {})

    def test_enumeration_becomes_a_literal(self) -> None:
        characteristic = Characteristic(
            urn="urn:test#C",
            kind="Enumeration",
            data_type=f"{XSD_PREFIX}string",
            values=("EV", "LMT"),
        )
        assert python_type(characteristic, {}) == "Literal['EV', 'LMT']"

    def test_a_trait_unwraps_to_its_base(self) -> None:
        base = Characteristic(urn="urn:test#B", kind="Text", data_type=f"{XSD_PREFIX}string")
        trait = Characteristic(urn="urn:test#T", kind="Trait", base=base, constraints=("urn:x#R",))
        assert python_type(trait, {}) == "str"


class TestCollapse:
    def test_embedded_newlines_are_flattened(self) -> None:
        # SAMM descriptions quote regulation text and embed newlines freely. Left
        # alone they break out of the generated string literal.
        assert collapse("one\n\ntwo   three\t") == "one two three"

    def test_none_is_empty(self) -> None:
        assert collapse(None) == ""
