"""The committed bindings must equal a fresh generation, byte for byte.

This is what makes "generated, never hand-edited" enforceable. Without it, an edit to
the generated file survives until the next regeneration silently reverts it, and the
gap between those two moments is where a bug lives that nobody can reproduce.

Determinism is a precondition. RDF is a set, so anything that iterates the graph
without imposing an order produces different bytes on different runs, and the check
above becomes a coin flip that fails CI at random.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from bpass.samm.generate import BINDINGS, TARGETS, main, render


class TestDeterminism:
    def test_two_generations_are_identical(self) -> None:
        assert render("battery_pass") == render("battery_pass")

    def test_the_committed_file_matches_a_fresh_generation(self) -> None:
        committed = (BINDINGS / "battery_pass.py").read_text(encoding="utf-8")
        assert committed == render("battery_pass")

    def test_check_mode_passes_on_the_committed_tree(self, capsys: pytest.CaptureFixture) -> None:
        assert main(["--check"]) == 0

    def test_check_mode_fails_on_a_stale_file(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        stale = tmp_path / "bindings"
        stale.mkdir()
        (stale / "battery_pass.py").write_text("# edited by hand\n", encoding="utf-8")
        monkeypatch.setattr("bpass.samm.generate.BINDINGS", stale)
        assert main(["--check"]) == 1


class TestTargets:
    def test_every_target_is_a_pinned_aspect(self, source_urns: tuple[str, ...]) -> None:
        for aspect_urn in TARGETS.values():
            model_urn = aspect_urn.split("#")[0]
            assert model_urn in source_urns
