"""What the walk has to get right about SAMM.

Each test here corresponds to a way of reading the specification that produces
bindings which compile, typecheck, and quietly serialise the wrong document.
"""

from __future__ import annotations

import pytest
from rdflib import Graph

from bpass.samm.model import ModelResolutionError, ResolvedModel, UnsupportedConstruct
from bpass.samm.walk import resolve, standard_characteristic

BATTERY_PASS_URN = "urn:samm:io.catenax.battery.battery_pass:6.1.0#BatteryPass"


class TestPropertyReferences:
    def test_payload_name_comes_from_the_reference_not_the_definition(
        self, model: ResolvedModel
    ) -> None:
        """The single most consequential detail in the SAMM specification for a binding.

        samm:payloadName sits on the blank node inside an enclosing samm:properties
        list. Read it off the property definition instead and the same property
        serialises under its model name everywhere, which is wrong in 105 places in
        this aspect model alone.
        """
        renamed = [
            (ref.definition.name, ref.serialised_name)
            for entity in model.entities
            for ref in entity.properties
            if ref.payload_name
        ]
        assert ("codeKey", "key") in renamed
        assert ("batteryCategory", "category") in renamed
        assert len(renamed) > 100

    def test_the_same_property_can_serialise_under_different_names(
        self, model: ResolvedModel
    ) -> None:
        by_urn: dict[str, set[str]] = {}
        for entity in model.entities:
            for ref in entity.properties:
                by_urn.setdefault(ref.definition.urn, set()).add(ref.serialised_name)
        # If this ever becomes empty the property above is untested by real data, and
        # the design that separates PropertyRef from Property is unjustified.
        assert any(len(names) > 1 for names in by_urn.values())

    def test_optionality_is_read_from_the_reference(self, model: ResolvedModel) -> None:
        by_name = {ref.definition.name: ref for ref in model.aspect.properties}
        assert by_name["specVersion"].optional is True
        assert by_name["identification"].optional is False


class TestDeclarationOrder:
    def test_aspect_properties_keep_their_declared_order(self, model: ResolvedModel) -> None:
        # samm:properties is an RDF collection, not a set. Iterating triples returns it
        # in store order, which is arbitrary and would make generation non-deterministic.
        names = [ref.definition.name for ref in model.aspect.properties]
        assert names[:5] == [
            "specVersion",
            "identification",
            "operation",
            "characteristics",
            "sustainability",
        ]

    def test_enumeration_values_keep_their_declared_order(self, model: ResolvedModel) -> None:
        values = _find_characteristic(model, "batteryCategory").values
        assert values == ("SLI", "LMT", "EV", "industrial", "portable", "incorporated")


class TestCharacteristics:
    def test_standard_characteristics_resolve_from_the_table(self, model: ResolvedModel) -> None:
        # samm-c:Text is defined by the meta-model, which this project does not vendor.
        # Nothing in the loaded graph describes it.
        assert _find_characteristic(model, "specVersion").kind == "Text"

    def test_traits_expose_their_base_and_record_their_constraints(
        self, model: ResolvedModel
    ) -> None:
        traits = [
            ref.definition.characteristic
            for entity in model.entities
            for ref in entity.properties
            if ref.definition.characteristic.kind == "Trait"
        ]
        assert traits, "the model does use traits"
        assert all(trait.base is not None for trait in traits)
        assert any(trait.constraints for trait in traits)

    def test_an_unknown_meta_model_characteristic_raises(self) -> None:
        # Resolving it to nothing would emit a field typed on a guess. It raises, and
        # the message names what to add and where.
        with pytest.raises(UnsupportedConstruct, match="Invented"):
            standard_characteristic("urn:samm:org.eclipse.esmf.samm:characteristic:2.1.0#Invented")


class TestResolutionFailures:
    def test_an_unpinned_aspect_raises_rather_than_returning_nothing(self, graph: Graph) -> None:
        with pytest.raises(ModelResolutionError, match="not an aspect"):
            resolve(graph, "urn:samm:io.catenax.not.pinned:1.0.0#Missing")

    def test_the_closure_is_complete(self, model: ResolvedModel) -> None:
        """Resolution succeeding at all is the closure check.

        A reference into a model that is not pinned raises rather than resolving to
        None, so a complete walk of the aspect proves every transitive dependency is
        present. Seven of the nine pinned models are reachable only through the
        generic passport.
        """
        assert len(model.entities) > 60
        assert len(model.source_urns) == 9


def _find_characteristic(model: ResolvedModel, property_name: str):
    for ref in model.aspect.properties:
        if ref.definition.name == property_name:
            return ref.definition.characteristic
    for entity in model.entities:
        for ref in entity.properties:
            if ref.definition.name == property_name:
                return ref.definition.characteristic
    raise AssertionError(f"{property_name} not found in the resolved model")
