"""Shared fixtures.

Loading nine Turtle files is about four thousand triples of parsing. Session-scoped so
the suite pays for it once rather than once per test.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from rdflib import Graph

from bpass.samm.loader import load_graph
from bpass.samm.model import ResolvedModel
from bpass.samm.walk import resolve

REPO = Path(__file__).resolve().parents[2]
BATTERY_PASS_URN = "urn:samm:io.catenax.battery.battery_pass:6.1.0#BatteryPass"
GEN = REPO / "samm-models" / "io.catenax.battery.battery_pass" / "6.1.0" / "gen"


@pytest.fixture(scope="session")
def graph() -> Graph:
    return load_graph()[0]


@pytest.fixture(scope="session")
def source_urns() -> tuple[str, ...]:
    return load_graph()[1]


@pytest.fixture(scope="session")
def model(graph: Graph, source_urns: tuple[str, ...]) -> ResolvedModel:
    return resolve(graph, BATTERY_PASS_URN, source_urns)


@pytest.fixture(scope="session")
def official_payload() -> dict:
    """The example payload the official Java SAMM toolchain generated."""
    return json.loads((GEN / "BatteryPass.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def official_schema() -> dict:
    """The JSON Schema the official Java SAMM toolchain generated."""
    return json.loads((GEN / "BatteryPass-schema.json").read_text(encoding="utf-8"))
