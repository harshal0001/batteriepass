"""The loader refuses to generate from a model that is not the one that was pinned.

Bindings carry a provenance header naming the models they came from. If generation
proceeds against a modified aspect model, that header is a lie, and the header is the
thing the whole pinning discipline exists to make true.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from bpass.samm.loader import DEFAULT_ROOT, load_graph, load_sources, split_urn
from bpass.samm.model import ModelResolutionError


@pytest.fixture
def pinned_tree(tmp_path: Path) -> Path:
    root = tmp_path / "samm-models"
    shutil.copytree(DEFAULT_ROOT, root)
    return root


class TestPinning:
    def test_nine_models_are_pinned(self) -> None:
        assert len(load_sources()) == 9

    def test_a_modified_aspect_model_is_refused(self, pinned_tree: Path) -> None:
        turtle = pinned_tree / "io.catenax.battery.battery_pass" / "6.1.0" / "BatteryPass.ttl"
        turtle.write_text(turtle.read_text(encoding="utf-8") + "\n# tampered\n", encoding="utf-8")
        with pytest.raises(ModelResolutionError, match="hash mismatch"):
            load_graph(pinned_tree)

    def test_a_manifest_that_disagrees_with_the_pin_is_refused(self, pinned_tree: Path) -> None:
        manifest = pinned_tree / "io.catenax.shared.uuid" / "2.0.0" / "manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["commit"] = "0" * 40
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(ModelResolutionError, match="manifest pins commit"):
            load_graph(pinned_tree)

    def test_a_deleted_file_is_refused(self, pinned_tree: Path) -> None:
        (pinned_tree / "io.catenax.batch" / "3.0.0" / "Batch.ttl").unlink()
        with pytest.raises(ModelResolutionError, match="missing"):
            load_graph(pinned_tree)


class TestUrnParsing:
    def test_a_model_urn_splits(self) -> None:
        assert split_urn("urn:samm:io.catenax.battery.battery_pass:6.1.0#BatteryPass") == (
            "io.catenax.battery.battery_pass",
            "6.1.0",
            "BatteryPass",
        )

    def test_meta_model_urns_are_not_models(self) -> None:
        # samm-c:Text is vocabulary. Treating it as a model would send the loader
        # looking for a pin that should not exist.
        assert split_urn("urn:samm:org.eclipse.esmf.samm:characteristic:2.1.0#Text") is None

    def test_a_non_samm_urn_is_rejected(self) -> None:
        assert split_urn("https://example.com/thing") is None
