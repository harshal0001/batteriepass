"""Emit Pydantic v2 source from the resolved model.

The output is committed and regenerated in CI, and the build fails on any diff. That
makes determinism a correctness property rather than a nicety: the same graph must
produce the same bytes, on any machine, in any Python version's dictionary ordering.
Everything here that looks fussy — sorted sets, explicit ordering, no reliance on
iteration order — exists for that reason.

The generated module is deliberately not run through a formatter. Doing so would make
the committed bytes depend on a formatter release, so a routine tooling bump would
show up as a spurious diff in generated code. The emitter formats its own output and
``pyproject.toml`` excludes ``bindings/`` from linting.

Two decisions about the shape of the bindings are worth naming.

**Fields are snake_case with an alias.** SAMM property names are lowerCamelCase.
Emitting them verbatim would give Python code that reads like JSON; emitting
snake_case without an alias would break the payload. So fields are snake_case,
``alias`` carries the payload name, and ``populate_by_name`` lets both work. Dumping
with ``by_alias=True`` reproduces the original payload exactly.

**Unknown keys are rejected.** ``extra="forbid"``. These bindings are a schema of
record for a regulated document. A payload carrying a field the aspect model does not
define is a payload built against a different version, and silently dropping it would
turn a version mismatch into missing data nobody notices.
"""

from __future__ import annotations

import keyword
import re
from collections import Counter

from bpass.samm.model import (
    Aspect,
    Characteristic,
    Documentation,
    Entity,
    PropertyRef,
    ResolvedModel,
    UnsupportedConstruct,
)

XSD_PREFIX = "http://www.w3.org/2001/XMLSchema#"

XSD_TO_PYTHON: dict[str, str] = {
    "string": "str",
    "anyURI": "str",
    "curie": "str",
    "hexBinary": "str",
    "base64Binary": "str",
    "boolean": "bool",
    "byte": "int",
    "short": "int",
    "int": "int",
    "integer": "int",
    "long": "int",
    "unsignedByte": "int",
    "unsignedShort": "int",
    "unsignedInt": "int",
    "unsignedLong": "int",
    "positiveInteger": "int",
    "nonNegativeInteger": "int",
    "negativeInteger": "int",
    "nonPositiveInteger": "int",
    "float": "float",
    "double": "float",
    "decimal": "float",
    "date": "date",
    "time": "time",
    "dateTime": "datetime",
    "dateTimeStamp": "datetime",
    "duration": "str",
    "langString": "str",
}

TYPING_IMPORTS = {"date", "time", "datetime"}

_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_NON_IDENTIFIER = re.compile(r"[^0-9a-zA-Z_]+")
_WHITESPACE = re.compile(r"\s+")


def snake_case(name: str) -> str:
    """lowerCamelCase to snake_case, kept reversible for the names SAMM produces."""
    snake = _CAMEL_BOUNDARY.sub("_", name)
    snake = _NON_IDENTIFIER.sub("_", snake).lower().strip("_")
    if not snake:
        raise UnsupportedConstruct("property name", name, "does not yield an identifier")
    if snake[0].isdigit():
        snake = f"n_{snake}"
    if keyword.iskeyword(snake) or keyword.issoftkeyword(snake):
        snake = f"{snake}_"
    return snake


def pascal_case(name: str) -> str:
    parts = [part for part in _NON_IDENTIFIER.sub("_", name).split("_") if part]
    return "".join(part[:1].upper() + part[1:] for part in parts)


def collapse(text: str | None) -> str:
    """One line, no runaway whitespace. SAMM descriptions embed newlines freely."""
    return "" if text is None else _WHITESPACE.sub(" ", text).strip()


def _namespace_prefix(urn: str) -> str:
    """Disambiguating prefix built from a model URN's last namespace segment."""
    namespace = urn.split("#", 1)[0].removeprefix("urn:samm:").rsplit(":", 1)[0]
    return pascal_case(namespace.rsplit(".", 1)[-1])


def class_names(model: ResolvedModel) -> dict[str, str]:
    """Map every entity URN to a unique Python class name.

    Local names are not unique across models. BatteryPass reaches two different
    ``IdentificationEntity`` definitions and two different ``KeyValueList`` ones. A
    generator that keys on the local name silently emits one and binds both, which
    typechecks and produces wrong data. Collisions are therefore resolved by
    qualifying with the defining model's namespace, and only the colliding names are
    qualified so that the common case stays readable.
    """
    counts = Counter(entity.name for entity in model.entities)
    names: dict[str, str] = {}
    for entity in model.entities:
        base = pascal_case(entity.name)
        if counts[entity.name] > 1:
            base = f"{_namespace_prefix(entity.urn)}{base}"
        if base in names.values():
            raise UnsupportedConstruct(
                "entity name collision",
                entity.urn,
                f"{base} is already taken and namespace qualification did not separate them",
            )
        names[entity.urn] = base
    return names


def _scalar(data_type: str | None, node: str) -> str:
    if data_type is None:
        raise UnsupportedConstruct("characteristic without a datatype", node)
    if not data_type.startswith(XSD_PREFIX):
        raise UnsupportedConstruct("non-XSD datatype", node, f"{data_type} is not a scalar")
    local = data_type.removeprefix(XSD_PREFIX)
    python = XSD_TO_PYTHON.get(local)
    if python is None:
        raise UnsupportedConstruct(f"xsd:{local}", node, "add it to XSD_TO_PYTHON")
    return python


def python_type(characteristic: Characteristic, names: dict[str, str]) -> str:
    """The annotation for one characteristic.

    Traits unwrap to their base characteristic. Their constraints are recorded in the
    field description rather than enforced: a regular-expression or range constraint
    from the aspect model is a statement about the upstream schema, and re-asserting
    it here would make these bindings reject payloads the schema of record accepts.
    """
    kind = characteristic.kind

    if kind == "Trait":
        if characteristic.base is None:
            raise UnsupportedConstruct("Trait without a base", characteristic.urn)
        return python_type(characteristic.base, names)

    if kind == "Enumeration":
        if not characteristic.values:
            raise UnsupportedConstruct("empty Enumeration", characteristic.urn)
        rendered = ", ".join(repr(value) for value in characteristic.values)
        return f"Literal[{rendered}]"

    if kind in {"List", "Set", "SortedSet"}:
        if characteristic.entity is not None:
            return f"list[{names[characteristic.entity.urn]}]"
        return f"list[{_scalar(characteristic.data_type, characteristic.urn)}]"

    if kind == "SingleEntity":
        if characteristic.entity is None:
            raise UnsupportedConstruct("SingleEntity without an entity", characteristic.urn)
        return names[characteristic.entity.urn]

    if characteristic.entity is not None:
        return names[characteristic.entity.urn]

    return _scalar(characteristic.data_type, characteristic.urn)


def _field_description(ref: PropertyRef) -> str:
    """Description, unit and constraint provenance, as one line."""
    characteristic = ref.definition.characteristic
    parts = [collapse(ref.definition.documentation.description)]

    unit_source = characteristic
    while unit_source.kind == "Trait" and unit_source.base is not None:
        unit_source = unit_source.base
    if unit_source.unit:
        parts.append(f"Unit: {unit_source.unit.rsplit('#', 1)[-1]}.")

    if characteristic.kind == "Trait" and characteristic.constraints:
        constrained = ", ".join(c.rsplit("#", 1)[-1] for c in characteristic.constraints)
        parts.append(f"Constrained upstream by {constrained}; not enforced here.")

    return " ".join(part for part in parts if part)


def _docstring(name: str, documentation: Documentation, indent: str) -> list[str]:
    title = collapse(documentation.preferred_name) or name
    description = collapse(documentation.description)
    lines = [f'{indent}"""{title}.']
    if description:
        lines.append("")
        lines.extend(_wrap(description, indent, width=88))
    for reference in documentation.see:
        lines.append("")
        lines.append(f"{indent}See {reference}")
    lines.append(f'{indent}"""')
    return lines


def _wrap(text: str, indent: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = indent
    for word in words:
        candidate = word if current == indent else f"{current} {word}"
        if current != indent and len(candidate) > width:
            lines.append(current)
            current = f"{indent}{word}"
        else:
            current = candidate if current != indent else f"{indent}{word}"
    if current.strip():
        lines.append(current)
    return lines


def _render_field(ref: PropertyRef, names: dict[str, str]) -> list[str]:
    field_name = snake_case(ref.definition.name)
    annotation = python_type(ref.definition.characteristic, names)
    if ref.optional:
        annotation = f"{annotation} | None"

    arguments = [f"        alias={ref.serialised_name!r},"]
    if ref.optional:
        arguments.append("        default=None,")
    description = _field_description(ref)
    if description:
        arguments.extend(f"        {line}" for line in _render_kwarg("description", description))
    arguments.append(f"        json_schema_extra={{'urn': {ref.definition.urn!r}}},")

    return [
        f"    {field_name}: {annotation} = Field(",
        *arguments,
        "    )",
    ]


def _render_kwarg(name: str, value: str) -> list[str]:
    """Render a long string keyword argument across lines, deterministically."""
    single = f"{name}={value!r},"
    if len(single) <= 88:
        return [single]
    chunks: list[str] = []
    remaining = value
    while remaining:
        cut = min(76, len(remaining))
        if cut < len(remaining):
            space = remaining.rfind(" ", 0, cut + 1)
            if space > 0:
                cut = space + 1
        chunks.append(remaining[:cut])
        remaining = remaining[cut:]
    lines = [f"{name}=("]
    lines.extend(f"    {chunk!r}" for chunk in chunks)
    lines.append("),")
    return lines


def _render_model(
    name: str,
    documentation: Documentation,
    properties: tuple[PropertyRef, ...],
    names: dict[str, str],
) -> list[str]:
    lines = [f"class {name}(BaseModel):"]
    lines.extend(_docstring(name, documentation, "    "))
    lines.append("")
    lines.append("    model_config = ConfigDict(populate_by_name=True, extra='forbid')")
    lines.append("")
    payload = [ref for ref in properties if not ref.not_in_payload]
    if not payload:
        lines.append("    pass")
        return lines
    for ref in payload:
        lines.extend(_render_field(ref, names))
        lines.append("")
    lines.pop()
    return lines


def _imports(model: ResolvedModel, names: dict[str, str]) -> list[str]:
    annotations = {python_type(ref.definition.characteristic, names) for ref in _all_refs(model)}
    joined = " ".join(annotations)
    lines = ["from __future__ import annotations", ""]
    datetime_imports = sorted(name for name in TYPING_IMPORTS if re.search(rf"\b{name}\b", joined))
    if datetime_imports:
        lines.append(f"from datetime import {', '.join(datetime_imports)}")
    if "Literal[" in joined:
        lines.append("from typing import Literal")
    if len(lines) > 2:
        lines.append("")
    lines.append("from pydantic import BaseModel, ConfigDict, Field")
    return lines


def _all_refs(model: ResolvedModel) -> list[PropertyRef]:
    refs = list(model.aspect.properties)
    for entity in model.entities:
        refs.extend(entity.properties)
    return refs


def _header(model: ResolvedModel) -> list[str]:
    aspect: Aspect = model.aspect
    lines = [
        '"""Generated from Catena-X SAMM aspect models. Do not edit.',
        "",
        f"Aspect:    {aspect.urn}",
        "",
        "Generated from these pinned models:",
    ]
    lines.extend(f"    {urn}" for urn in model.source_urns)
    lines.extend(
        [
            "",
            "Regenerate with:",
            "",
            "    python -m bpass.samm.generate",
            "",
            "Every field carries its semantic URN in json_schema_extra, and its payload",
            "name as an alias. Dump with by_alias=True to reproduce a Catena-X payload.",
            '"""',
            "",
        ]
    )
    return lines


def emit(model: ResolvedModel) -> str:
    """Render the whole module. Pure: same input, same bytes, every time."""
    names = class_names(model)
    entity_by_urn: dict[str, Entity] = {entity.urn: entity for entity in model.entities}

    lines = _header(model)
    lines.extend(_imports(model, names))
    lines.append("")

    for urn in names:
        lines.append("")
        lines.extend(
            _render_model(
                names[urn], entity_by_urn[urn].documentation, entity_by_urn[urn].properties, names
            )
        )
        lines.append("")

    lines.append("")
    lines.extend(
        _render_model(
            pascal_case(model.aspect.name),
            model.aspect.documentation,
            model.aspect.properties,
            names,
        )
    )
    lines.append("")
    return "\n".join(lines)
