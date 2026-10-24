"""Resolve a rule set path against the generated bindings.

A rule set path such as ``performance.rated.capacity`` names a place in the passport
using payload names — the keys that appear in JSON — rather than Python field names.
That is the right choice for rule data: it stays readable next to the regulation text
and it survives a change in how the generator mangles names.

It also means the mapping can silently rot. The aspect model is versioned upstream
and regenerated whenever it moves; a path that pointed at something real in
BatteryPass 6.1.0 may point at nothing in 7.0.0. A rule whose path resolves to
nothing counts as a missing attribute forever and never says why, so resolution is
checked against the schema rather than only against payloads.
"""

from __future__ import annotations

from types import UnionType
from typing import Union, get_args, get_origin

from pydantic import BaseModel


class PathError(Exception):
    """A rule set path that does not exist in the bindings."""


def _unwrap(annotation: object) -> object:
    """Strip Optional and collection wrappers down to the underlying type.

    ``list[Foo]`` and ``Foo | None`` both address ``Foo`` for the purpose of a path.
    Whether a field is a list or an option is the conformance engine's business, not
    the resolver's.
    """
    seen: set[int] = set()
    while True:
        if id(annotation) in seen:
            return annotation
        seen.add(id(annotation))

        origin = get_origin(annotation)
        arguments = [arg for arg in get_args(annotation) if arg is not type(None)]

        if origin in (Union, UnionType):
            if len(arguments) != 1:
                return annotation
            annotation = arguments[0]
            continue
        if origin in (list, set, frozenset, tuple) and arguments:
            annotation = arguments[0]
            continue
        return annotation


def _field_by_payload_name(model: type[BaseModel], name: str) -> object | None:
    for field_name, field in model.model_fields.items():
        if (field.alias or field_name) == name:
            return field.annotation
    return None


def resolve(root: type[BaseModel], path: str) -> object:
    """Return the annotation a dotted payload path addresses.

    Raises :class:`PathError` naming the segment that failed, because "the path is
    wrong" is not actionable and "no field 'capacty' on RatedEntity" is.
    """
    if not path:
        raise PathError("empty path")

    current: object = root
    walked: list[str] = []

    for segment in path.split("."):
        model = _unwrap(current)
        if not (isinstance(model, type) and issubclass(model, BaseModel)):
            where = ".".join(walked) or "the passport root"
            raise PathError(f"{path}: {where} is a scalar, so it has no field {segment!r}")

        annotation = _field_by_payload_name(model, segment)
        if annotation is None:
            available = sorted((field.alias or name) for name, field in model.model_fields.items())
            where = ".".join(walked) or model.__name__
            raise PathError(
                f"{path}: no field {segment!r} on {where}. Available: {', '.join(available)}"
            )

        walked.append(segment)
        current = annotation

    return _unwrap(current)


def exists(root: type[BaseModel], path: str) -> bool:
    try:
        resolve(root, path)
    except PathError:
        return False
    return True


def unresolvable(root: type[BaseModel], paths: tuple[str, ...]) -> list[str]:
    """Every path that does not resolve, with the reason. Empty means all are sound."""
    problems: list[str] = []
    for path in paths:
        try:
            resolve(root, path)
        except PathError as exc:
            problems.append(str(exc))
    return problems
