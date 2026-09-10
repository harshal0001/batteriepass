"""The resolved SAMM model this generator emits from.

An intermediate representation, deliberately. The alternative — walking the RDF graph
and writing Python source in the same pass — makes two hard things simultaneous and
makes neither testable on its own. Splitting them means the walk can be checked
against the Turtle and the emitter can be checked against fixtures.

The shapes here follow SAMM 2.1.0 and stop where the BatteryPass aspect model stops.
That scope is a decision, not an oversight: a complete SAMM implementation is not the
deliverable. What matters is that the boundary is loud. An unsupported construct
raises :class:`UnsupportedConstruct`; nothing here ever degrades to ``Any``, because a
generator that quietly emits ``Any`` produces bindings that typecheck and lie.

One subtlety drives the design. ``samm:payloadName`` and ``samm:optional`` are
declared on the *reference* to a property inside an enclosing ``samm:properties``
list, not on the property definition. The same property can therefore appear as
``batteryCategory`` in one entity and be serialised as ``category`` in another. So
:class:`PropertyRef` and :class:`Property` are separate types, and the reference owns
the payload name.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class SammError(Exception):
    """Base for everything this package raises."""


class UnsupportedConstruct(SammError):
    """A SAMM construct outside the supported subset.

    Raised rather than worked around. The message names the construct and the node so
    that widening the subset is a small, obvious change.
    """

    def __init__(self, construct: str, node: str, hint: str = "") -> None:
        message = f"unsupported SAMM construct {construct} on {node}"
        if hint:
            message = f"{message}. {hint}"
        super().__init__(message)
        self.construct = construct
        self.node = node


class ModelResolutionError(SammError):
    """A reference that cannot be resolved: a missing import or a dangling URN."""


@dataclass(frozen=True)
class Documentation:
    """Human-facing text carried through to the generated docstrings.

    English only. SAMM allows any language tag and the BatteryPass model supplies
    ``@en`` throughout; picking a language at generation time rather than carrying all
    of them keeps the emitted code readable.
    """

    preferred_name: str | None = None
    description: str | None = None
    see: tuple[str, ...] = ()


@dataclass(frozen=True)
class Characteristic:
    """What a property's values look like.

    ``kind`` names the SAMM characteristic class in short form — ``Text``,
    ``Measurement``, ``List``, ``Enumeration``, ``SingleEntity``, ``Trait`` — and the
    remaining fields carry whatever that kind needs. A tagged union expressed as one
    frozen dataclass, because the emitter switches on ``kind`` exactly once.
    """

    urn: str
    kind: str
    documentation: Documentation = field(default_factory=Documentation)

    data_type: str | None = None
    """XSD datatype URI, or the URN of an Entity for SingleEntity and collections."""

    element: Characteristic | None = None
    """Element characteristic for List, Set and SortedSet."""

    entity: Entity | None = None
    """Resolved entity for SingleEntity and for collections of entities."""

    unit: str | None = None
    """Unit URN for Measurement and Quantifiable, e.g. ``unit:percent``."""

    values: tuple[str, ...] = ()
    """Permitted values for Enumeration, in declaration order."""

    base: Characteristic | None = None
    """Base characteristic for Trait. Constraints are recorded, never enforced."""

    constraints: tuple[str, ...] = ()
    """URNs of the constraints on a Trait, for provenance in the docstring."""


@dataclass(frozen=True)
class Property:
    """A SAMM property definition.

    Note what is *not* here: optionality and payload name. Both belong to the
    reference, not the definition. See the module docstring.
    """

    urn: str
    name: str
    characteristic: Characteristic
    documentation: Documentation = field(default_factory=Documentation)
    example_value: str | None = None


@dataclass(frozen=True)
class PropertyRef:
    """One property as used by one aspect or entity.

    ``payload_name`` is the key that appears in JSON. ``name`` is the key in the
    model. When they differ, the generated field carries an alias, and round-tripping
    a payload depends on getting this right.
    """

    definition: Property
    """The property being referenced. Named ``definition`` rather than ``property``
    because a field called ``property`` shadows the builtin inside the class body,
    which breaks the decorator below."""

    optional: bool = False
    payload_name: str | None = None
    not_in_payload: bool = False

    @property
    def serialised_name(self) -> str:
        return self.payload_name or self.definition.name


@dataclass(frozen=True)
class Entity:
    """A named structure of properties. Becomes one generated Pydantic model."""

    urn: str
    name: str
    properties: tuple[PropertyRef, ...]
    documentation: Documentation = field(default_factory=Documentation)
    extends: str | None = None


@dataclass(frozen=True)
class Aspect:
    """The root of an aspect model. Becomes the top-level generated Pydantic model."""

    urn: str
    name: str
    namespace: str
    version: str
    properties: tuple[PropertyRef, ...]
    documentation: Documentation = field(default_factory=Documentation)


@dataclass(frozen=True)
class ResolvedModel:
    """Everything the emitter needs: one aspect and every entity reachable from it.

    ``entities`` is ordered so that a definition always precedes its first use, which
    is what lets the emitter write a single module with no forward references and no
    ``model_rebuild()`` call.
    """

    aspect: Aspect
    entities: tuple[Entity, ...]
    source_urns: tuple[str, ...]
    """Every model URN that contributed, in load order. Recorded in the generated
    header so a binding can always name the models it came from."""
