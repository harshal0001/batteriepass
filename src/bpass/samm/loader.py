"""Load the pinned aspect models into one RDF graph.

Everything is loaded together rather than one model at a time. SAMM references cross
model boundaries freely — BatteryPass 6.1.0 reaches into the generic passport, which
reaches into seven more — and a per-model graph would turn every one of those into a
resolution step. One graph makes a cross-model reference indistinguishable from a
local one, which is what it is.

Hashes are verified here as well as in ``scripts/fetch_samm.py``. That looks like
duplication and is not: the script guards the working tree, this guards the act of
generating. Bindings produced from an aspect model that does not match its manifest
would carry a provenance header that is a lie, and the header is the thing the whole
pinning discipline exists to make true.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from rdflib import Graph, Namespace

from bpass.samm.model import ModelResolutionError

SAMM = Namespace("urn:samm:org.eclipse.esmf.samm:meta-model:2.1.0#")
SAMM_C = Namespace("urn:samm:org.eclipse.esmf.samm:characteristic:2.1.0#")
SAMM_E = Namespace("urn:samm:org.eclipse.esmf.samm:entity:2.1.0#")
UNIT = Namespace("urn:samm:org.eclipse.esmf.samm:unit:2.1.0#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

MODEL_URN = re.compile(r"^urn:samm:(?P<namespace>[^:]+):(?P<version>[^#]+)#(?P<name>.*)$")

DEFAULT_ROOT = Path(__file__).resolve().parents[3] / "samm-models"


@dataclass(frozen=True)
class PinnedModel:
    namespace: str
    version: str
    commit: str
    aspect: str
    directory: Path

    @property
    def urn(self) -> str:
        return f"urn:samm:{self.namespace}:{self.version}"

    @property
    def aspect_urn(self) -> str:
        return f"{self.urn}#{self.aspect}"


def split_urn(urn: str) -> tuple[str, str, str] | None:
    """Split a SAMM URN into namespace, version and local name.

    Returns ``None`` for anything that is not a SAMM model URN, including the
    meta-model namespaces, which are vocabulary rather than models.
    """
    match = MODEL_URN.match(urn)
    if match is None:
        return None
    namespace = match["namespace"]
    if namespace.startswith("org.eclipse.esmf.samm"):
        return None
    return namespace, match["version"], match["name"]


def load_sources(root: Path = DEFAULT_ROOT) -> list[PinnedModel]:
    sources = root / "sources.json"
    if not sources.is_file():
        raise ModelResolutionError(
            f"{sources} not found. Run scripts/fetch_samm.py to pin the aspect models."
        )
    data = json.loads(sources.read_text(encoding="utf-8"))
    return [
        PinnedModel(
            namespace=entry["namespace"],
            version=entry["version"],
            commit=entry["commit"],
            aspect=entry["aspect"],
            directory=root / entry["namespace"] / entry["version"],
        )
        for entry in data["models"]
    ]


def _verify(model: PinnedModel) -> dict[str, str]:
    """Check every file against the manifest. Return the manifest's file hashes."""
    manifest_path = model.directory / "manifest.json"
    if not manifest_path.is_file():
        raise ModelResolutionError(
            f"{model.namespace} {model.version}: no manifest. Run scripts/fetch_samm.py."
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("commit") != model.commit:
        raise ModelResolutionError(
            f"{model.namespace} {model.version}: manifest pins commit "
            f"{manifest.get('commit')}, sources.json pins {model.commit}"
        )
    files: dict[str, str] = manifest["files"]
    for relative, expected in files.items():
        path = model.directory / relative
        if not path.is_file():
            raise ModelResolutionError(f"{path}: pinned but missing")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ModelResolutionError(
                f"{path}: hash mismatch against the manifest. Refusing to generate "
                f"bindings from an aspect model that is not the one that was pinned."
            )
    return files


def load_graph(root: Path = DEFAULT_ROOT) -> tuple[Graph, tuple[str, ...]]:
    """Parse every pinned Turtle file into one graph.

    Returns the graph and the URNs that contributed, in ``sources.json`` order, so the
    generated header can name exactly what it was built from.
    """
    graph = Graph()
    urns: list[str] = []
    for model in load_sources(root):
        files = _verify(model)
        for relative in sorted(files):
            if relative.endswith(".ttl"):
                graph.parse(model.directory / relative, format="turtle")
        urns.append(model.urn)

    graph.bind("samm", SAMM)
    graph.bind("samm-c", SAMM_C)
    graph.bind("samm-e", SAMM_E)
    graph.bind("unit", UNIT)
    return graph, tuple(urns)
