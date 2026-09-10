"""Does this generator agree with the official one?

There is no Python SAMM toolchain, which is why this generator exists. That also means
there is nothing to compare it against — except that the upstream repository publishes
the output of the official Java toolchain beside every aspect model. Those artefacts
are the reference, and checking against them costs no JVM and no network.

Three claims, in increasing strength:

1. The official example payload validates against our generated bindings.
2. Dumping it back produces the same keys in the same structure — which is the claim
   that every alias, every optionality and every nesting decision is right.
3. That output validates against the JSON Schema the official toolchain generated.

Claim 3 is the one that matters. It says a Catena-X consumer would accept what we
produce, judged by the ecosystem's own schema rather than by our reading of it.
"""

from __future__ import annotations

from datetime import datetime

import pytest
from jsonschema import Draft4Validator

from bpass.bindings.battery_pass import BatteryPass


def key_structure(value: object) -> object:
    """Strip scalar values, keep keys, nesting and types.

    Used to separate "the shape is right" from "the bytes are identical". The shape is
    what the generator controls; some of the bytes are the JSON writer's business.
    """
    if isinstance(value, dict):
        return {key: key_structure(inner) for key, inner in sorted(value.items())}
    if isinstance(value, list):
        return [key_structure(item) for item in value]
    return type(value).__name__


@pytest.fixture(scope="module")
def dumped(official_payload: dict) -> dict:
    parsed = BatteryPass.model_validate(official_payload)
    result: dict = parsed.model_dump(by_alias=True, mode="json", exclude_none=True)
    return result


class TestOfficialExample:
    def test_the_official_payload_validates(self, official_payload: dict) -> None:
        assert BatteryPass.model_validate(official_payload) is not None

    def test_key_structure_survives_the_round_trip(
        self, dumped: dict, official_payload: dict
    ) -> None:
        # Every alias, every optional field and every nesting level. 105 of the
        # properties in this model serialise under a name that differs from the one
        # the aspect model declares; getting any of them wrong shows up here.
        assert key_structure(dumped) == key_structure(official_payload)

    def test_the_round_trip_is_lossless(self, dumped: dict, official_payload: dict) -> None:
        # Model equality rather than byte equality, because the two are not the same
        # question. See test_timestamps_differ_only_in_lexical_form below.
        assert BatteryPass.model_validate(dumped) == BatteryPass.model_validate(official_payload)

    def test_bytes_differ_only_in_timestamp_lexical_form(
        self, dumped: dict, official_payload: dict
    ) -> None:
        """The one place the bytes differ, and why that is correct.

        xsd:dateTime has no canonical width for fractional seconds. The official
        payload writes ``.576``; Python's isoformat writes ``.576000``. Same instant,
        both valid lexical forms. Asserting byte equality here would be asserting
        something XML Schema does not require, so the assertion is that every
        difference is of exactly this kind — and that there are no others.
        """
        differences = list(_differences(dumped, official_payload))
        assert differences, "expected the known timestamp differences; found none"
        for path, ours, theirs in differences:
            assert datetime.fromisoformat(str(ours)) == datetime.fromisoformat(str(theirs)), (
                f"{path} differs by more than lexical form: {ours!r} vs {theirs!r}"
            )


class TestOfficialSchema:
    def test_the_official_example_validates_against_the_official_schema(
        self, official_schema: dict, official_payload: dict
    ) -> None:
        # A control. If this ever fails, the reference moved and the tests below say
        # nothing. Note the draft: the schema declares draft-04, where
        # exclusiveMaximum is a boolean modifier rather than a bound. Validating it as
        # 2020-12 reports eight spurious errors on the official file itself.
        assert official_schema["$schema"] == "http://json-schema.org/draft-04/schema"
        assert Draft4Validator(official_schema).is_valid(official_payload)

    def test_our_output_validates_against_the_official_schema(
        self, official_schema: dict, dumped: dict
    ) -> None:
        errors = sorted(Draft4Validator(official_schema).iter_errors(dumped), key=lambda e: e.path)
        assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors[:10])


class TestSemanticProvenance:
    def test_every_field_carries_its_urn(self) -> None:
        """The semantic URN is the point of binding to SAMM rather than to a schema.

        Without it a field is just a name; with it, a consumer can resolve what the
        field means back to the aspect model that defines it.
        """
        missing = [
            name
            for name, field in BatteryPass.model_fields.items()
            if not (field.json_schema_extra or {}).get("urn")  # type: ignore[union-attr]
        ]
        assert missing == []

    def test_urns_point_at_pinned_models(self, source_urns: tuple[str, ...]) -> None:
        for field in BatteryPass.model_fields.values():
            urn = (field.json_schema_extra or {})["urn"]  # type: ignore[index]
            assert any(str(urn).startswith(source) for source in source_urns)


def _differences(ours: object, theirs: object, path: str = "") -> object:
    if isinstance(ours, dict) and isinstance(theirs, dict):
        for key in sorted(set(ours) | set(theirs)):
            yield from _differences(ours.get(key), theirs.get(key), f"{path}.{key}")
    elif isinstance(ours, list) and isinstance(theirs, list):
        for index, (a, b) in enumerate(zip(ours, theirs, strict=True)):
            yield from _differences(a, b, f"{path}[{index}]")
    elif ours != theirs:
        yield path, ours, theirs
