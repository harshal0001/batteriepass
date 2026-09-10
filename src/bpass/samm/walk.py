"""Walk the RDF graph into the intermediate representation.

This is the half of the generator that has to be right about SAMM. The emitter that
follows it only has to be right about Python.

Three things here are easy to get wrong and produce bindings that look correct.

**Property references carry the payload contract.** ``samm:payloadName`` and
``samm:optional`` live on the blank node inside an enclosing ``samm:properties``
list, not on the property definition. Read them off the definition and a payload
round-trips as ``batteryCategory`` where the aspect model says ``category``.

**Order is part of the model.** ``samm:properties`` is an RDF collection, not a set.
Iterating the graph's triples returns it in whatever order the store feels like,
which makes the generated output non-deterministic and the regeneration check
useless. Collections are read as collections.

**Standard characteristics are not in the graph.** ``samm-c:Text`` and its siblings
are defined by the SAMM meta-model, which this project does not vendor. They are
resolved from a table below. Anything else in the ``samm-c`` namespace that is not in
that table raises rather than resolving to nothing.
"""

from __future__ import annotations

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.term import Node

from bpass.samm.loader import SAMM, SAMM_C, XSD, split_urn
from bpass.samm.model import (
    Aspect,
    Characteristic,
    Documentation,
    Entity,
    ModelResolutionError,
    Property,
    PropertyRef,
    ResolvedModel,
    UnsupportedConstruct,
)

# Characteristic instances defined by the SAMM meta-model itself. They appear in
# aspect models as bare references with no local definition, so the graph cannot
# answer what they mean.
STANDARD_CHARACTERISTICS: dict[str, tuple[str, str]] = {
    "Text": ("Text", str(XSD.string)),
    "Boolean": ("Boolean", str(XSD.boolean)),
    "Timestamp": ("Timestamp", str(XSD.dateTime)),
    "MultiLanguageText": ("MultiLanguageText", str(XSD.string)),
    "Locale": ("Text", str(XSD.string)),
    "Language": ("Text", str(XSD.string)),
    "MimeType": ("Text", str(XSD.string)),
    "ResourcePath": ("Text", str(XSD.anyURI)),
    "UnitReference": ("Text", str(XSD.string)),
}

# SAMM characteristic classes this generator understands, mapped to the ``kind`` the
# emitter switches on. Anything outside this set raises.
CHARACTERISTIC_CLASSES: dict[str, str] = {
    "Characteristic": "Characteristic",
    "Enumeration": "Enumeration",
    "List": "List",
    "Set": "Set",
    "SortedSet": "SortedSet",
    "Measurement": "Measurement",
    "Quantifiable": "Quantifiable",
    "Trait": "Trait",
    "SingleEntity": "SingleEntity",
    "Duration": "Measurement",
    "Code": "Characteristic",
    "State": "Enumeration",
}

COLLECTION_KINDS = frozenset({"List", "Set", "SortedSet"})


def _local_name(node: Node) -> str:
    text = str(node)
    return text.rsplit("#", 1)[-1] if "#" in text else text.rsplit("/", 1)[-1]


def _english(graph: Graph, subject: Node, predicate: URIRef) -> str | None:
    """First English literal for a predicate, falling back to an untagged one.

    SAMM permits any language tag. The Catena-X models supply ``@en`` throughout, and
    carrying every translation into generated docstrings would bloat them for no gain.
    """
    untagged: str | None = None
    for value in graph.objects(subject, predicate):
        if not isinstance(value, Literal):
            continue
        if value.language == "en":
            return str(value)
        if value.language is None and untagged is None:
            untagged = str(value)
    return untagged


def _documentation(graph: Graph, subject: Node) -> Documentation:
    return Documentation(
        preferred_name=_english(graph, subject, SAMM.preferredName),
        description=_english(graph, subject, SAMM.description),
        see=tuple(sorted(str(value) for value in graph.objects(subject, SAMM.see))),
    )


def _collection(graph: Graph, node: Node) -> list[Node]:
    """Read an RDF collection in declaration order.

    An empty collection is ``rdf:nil``, which is a URIRef rather than a list node, so
    it is handled explicitly instead of failing inside rdflib's Collection.
    """
    if str(node).endswith("#nil"):
        return []
    return list(Collection(graph, node))


def standard_characteristic(urn: str) -> Characteristic:
    """Resolve a characteristic defined by the SAMM meta-model rather than by a model.

    ``samm-c:Text`` and its siblings are vocabulary, not model content. This project
    does not vendor the meta-model, so nothing in the loaded graph describes them and
    they are resolved from the table above. Anything in the ``samm-c`` namespace that
    is not in the table raises: resolving it to nothing would emit a field typed
    ``str`` on a guess.
    """
    name = _local_name(URIRef(urn))
    entry = STANDARD_CHARACTERISTICS.get(name)
    if entry is None:
        raise UnsupportedConstruct(
            f"samm-c:{name}",
            urn,
            "it is a meta-model characteristic this generator does not model. Add it "
            "to STANDARD_CHARACTERISTICS with its datatype.",
        )
    kind, data_type = entry
    return Characteristic(urn=urn, kind=kind, data_type=data_type)


class Walker:
    """Resolves one aspect and everything reachable from it.

    Stateful because entities and characteristics are shared and must be resolved
    once. The memo is also what keeps a mutually referential pair of entities from
    recursing forever.
    """

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self._entities: dict[str, Entity] = {}
        self._characteristics: dict[str, Characteristic] = {}
        self._order: list[str] = []
        self._in_progress: set[str] = set()

    # -- entry point ----------------------------------------------------------

    def resolve_aspect(self, urn: str) -> tuple[Aspect, tuple[Entity, ...]]:
        node = URIRef(urn)
        if (node, SAMM.properties, None) not in self.graph:
            raise ModelResolutionError(
                f"{urn} is not an aspect in the loaded graph. Check that its model is "
                f"pinned in samm-models/sources.json."
            )
        parts = split_urn(urn)
        if parts is None:
            raise ModelResolutionError(f"{urn} is not a SAMM model URN")
        namespace, version, name = parts

        aspect = Aspect(
            urn=urn,
            name=name,
            namespace=namespace,
            version=version,
            properties=self._property_refs(node),
            documentation=_documentation(self.graph, node),
        )
        # self._order records first-definition order, which is dependency order because
        # an entity is only appended once its own properties have resolved.
        return aspect, tuple(self._entities[key] for key in self._order)

    # -- properties -----------------------------------------------------------

    def _property_refs(self, subject: Node) -> tuple[PropertyRef, ...]:
        listing = self.graph.value(subject, SAMM.properties)
        if listing is None:
            return ()
        return tuple(self._property_ref(entry) for entry in _collection(self.graph, listing))

    def _property_ref(self, entry: Node) -> PropertyRef:
        if isinstance(entry, URIRef):
            return PropertyRef(definition=self._property(entry))

        if not isinstance(entry, BNode):
            raise UnsupportedConstruct("property reference", str(entry))

        target = self.graph.value(entry, SAMM.property)
        if not isinstance(target, URIRef):
            raise UnsupportedConstruct(
                "property reference",
                str(entry),
                "a blank node in samm:properties must carry samm:property",
            )

        payload_name = self.graph.value(entry, SAMM.payloadName)
        return PropertyRef(
            definition=self._property(target),
            optional=bool(self.graph.value(entry, SAMM.optional)),
            payload_name=str(payload_name) if payload_name is not None else None,
            not_in_payload=bool(self.graph.value(entry, SAMM.notInPayload)),
        )

    def _property(self, node: URIRef) -> Property:
        characteristic = self.graph.value(node, SAMM.characteristic)
        if characteristic is None:
            raise ModelResolutionError(
                f"{node} has no samm:characteristic. Its model is probably not pinned; "
                f"add it to samm-models/sources.json."
            )
        example = self.graph.value(node, SAMM.exampleValue)
        return Property(
            urn=str(node),
            name=_local_name(node),
            characteristic=self._characteristic(characteristic),
            documentation=_documentation(self.graph, node),
            example_value=str(example) if example is not None else None,
        )

    # -- characteristics ------------------------------------------------------

    def _characteristic(self, node: Node) -> Characteristic:
        urn = str(node)
        cached = self._characteristics.get(urn)
        if cached is not None:
            return cached

        if urn.startswith(str(SAMM_C)):
            resolved = standard_characteristic(urn)
        else:
            resolved = self._declared_characteristic(node)
        self._characteristics[urn] = resolved
        return resolved

    def _declared_characteristic(self, node: Node) -> Characteristic:
        kind = self._characteristic_kind(node)
        documentation = _documentation(self.graph, node)
        data_type = self.graph.value(node, SAMM.dataType)

        if kind == "Trait":
            base = self.graph.value(node, SAMM_C.baseCharacteristic)
            if base is None:
                raise ModelResolutionError(f"{node} is a Trait with no baseCharacteristic")
            return Characteristic(
                urn=str(node),
                kind="Trait",
                documentation=documentation,
                base=self._characteristic(base),
                constraints=tuple(
                    sorted(str(c) for c in self.graph.objects(node, SAMM_C.constraint))
                ),
            )

        if kind == "Enumeration":
            values = self.graph.value(node, SAMM_C.values)
            if values is None:
                raise ModelResolutionError(f"{node} is an Enumeration with no samm-c:values")
            return Characteristic(
                urn=str(node),
                kind="Enumeration",
                documentation=documentation,
                data_type=str(data_type) if data_type is not None else None,
                values=tuple(str(v) for v in _collection(self.graph, values)),
            )

        if kind in COLLECTION_KINDS:
            if data_type is None:
                raise ModelResolutionError(f"{node} is a {kind} with no samm:dataType")
            return Characteristic(
                urn=str(node),
                kind=kind,
                documentation=documentation,
                data_type=str(data_type),
                entity=self._entity_if_any(data_type),
            )

        if kind in {"Measurement", "Quantifiable"}:
            unit = self.graph.value(node, SAMM_C.unit)
            return Characteristic(
                urn=str(node),
                kind=kind,
                documentation=documentation,
                data_type=str(data_type) if data_type is not None else None,
                unit=str(unit) if unit is not None else None,
            )

        if data_type is None:
            raise ModelResolutionError(f"{node} is a Characteristic with no samm:dataType")

        entity = self._entity_if_any(data_type)
        return Characteristic(
            urn=str(node),
            kind="SingleEntity" if entity is not None else "Characteristic",
            documentation=documentation,
            data_type=str(data_type),
            entity=entity,
        )

    def _characteristic_kind(self, node: Node) -> str:
        types = [_local_name(t) for t in self.graph.objects(node, URIRef(f"{SAMM}type"))]
        types += [
            _local_name(t)
            for t in self.graph.objects(
                node, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
            )
        ]
        for name in types:
            mapped = CHARACTERISTIC_CLASSES.get(name)
            if mapped is not None:
                return mapped
        if types:
            raise UnsupportedConstruct(
                f"characteristic class {types[0]}",
                str(node),
                "add it to CHARACTERISTIC_CLASSES once the emitter can render it.",
            )
        raise ModelResolutionError(
            f"{node} has no rdf:type. Its model is probably not pinned; add it to "
            f"samm-models/sources.json."
        )

    # -- entities -------------------------------------------------------------

    def _entity_if_any(self, node: Node) -> Entity | None:
        """Resolve a datatype that names an Entity. XSD datatypes return None."""
        if not isinstance(node, URIRef) or str(node).startswith(str(XSD)):
            return None
        if (node, SAMM.properties, None) not in self.graph:
            return None
        return self._entity(node)

    def _entity(self, node: URIRef) -> Entity:
        urn = str(node)
        cached = self._entities.get(urn)
        if cached is not None:
            return cached
        if urn in self._in_progress:
            raise UnsupportedConstruct(
                "recursive entity",
                urn,
                "this generator emits a single module with no forward references, "
                "which a cycle would require.",
            )

        self._in_progress.add(urn)
        try:
            entity = Entity(
                urn=urn,
                name=_local_name(node),
                properties=self._property_refs(node),
                documentation=_documentation(self.graph, node),
            )
        finally:
            self._in_progress.discard(urn)

        self._entities[urn] = entity
        self._order.append(urn)
        return entity


def resolve(graph: Graph, aspect_urn: str, source_urns: tuple[str, ...] = ()) -> ResolvedModel:
    """Resolve one aspect and every entity reachable from it."""
    aspect, entities = Walker(graph).resolve_aspect(aspect_urn)
    return ResolvedModel(aspect=aspect, entities=entities, source_urns=source_urns)
