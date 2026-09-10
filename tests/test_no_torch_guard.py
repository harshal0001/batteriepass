"""The boundary guard is the only thing standing between the image and 700 MB.

A guard that silently stops detecting is worse than no guard, so it is tested the
way a lint rule should be: feed it code that breaks the rule and require it to say so.
"""

from __future__ import annotations

from pathlib import Path

from no_torch_in_src import banned_imports, check_runtime_dependencies, check_sources


def write(tmp_path: Path, name: str, body: str) -> Path:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return path


class TestImportDetection:
    def test_plain_import(self, tmp_path: Path) -> None:
        path = write(tmp_path, "m.py", "import torch\n")
        assert banned_imports(path) == [(1, "torch")]

    def test_aliased_import_is_not_a_loophole(self, tmp_path: Path) -> None:
        path = write(tmp_path, "m.py", "import torch as t\n")
        assert banned_imports(path) == [(1, "torch")]

    def test_submodule_import(self, tmp_path: Path) -> None:
        path = write(tmp_path, "m.py", "from torch.nn import Linear\n")
        assert banned_imports(path) == [(1, "torch")]

    def test_import_nested_inside_a_function_still_counts(self, tmp_path: Path) -> None:
        # A lazy import is the most likely way this rule gets broken in practice:
        # it looks harmless because the module still imports fast.
        path = write(tmp_path, "m.py", "def f():\n    import torch\n    return torch\n")
        assert banned_imports(path) == [(2, "torch")]

    def test_the_word_torch_in_prose_is_not_an_import(self, tmp_path: Path) -> None:
        # Grep would fail this. This module's own docstring is the reason it matters.
        path = write(tmp_path, "m.py", '"""We never import torch here."""\nX = "torch"\n')
        assert banned_imports(path) == []

    def test_a_lookalike_package_is_not_banned(self, tmp_path: Path) -> None:
        path = write(tmp_path, "m.py", "import torchmetrics_lite_unrelated\n")
        assert banned_imports(path) == []

    def test_relative_imports_are_ignored(self, tmp_path: Path) -> None:
        path = write(tmp_path, "m.py", "from . import torch\n")
        assert banned_imports(path) == []


class TestSourceTree:
    def test_the_real_src_tree_is_clean(self) -> None:
        repo = Path(__file__).resolve().parent.parent
        assert check_sources(repo / "src") == []

    def test_training_is_exempt(self, tmp_path: Path) -> None:
        (tmp_path / "training").mkdir()
        write(tmp_path / "training", "train.py", "import torch\n")
        assert check_sources(tmp_path) == []


class TestRuntimeDependencies:
    def test_the_real_pyproject_is_clean(self) -> None:
        repo = Path(__file__).resolve().parent.parent
        assert check_runtime_dependencies(repo / "pyproject.toml") == []

    def test_a_pinned_torch_dependency_is_caught(self, tmp_path: Path) -> None:
        path = write(
            tmp_path,
            "pyproject.toml",
            '[project]\nname = "x"\ndependencies = ["fastapi>=0.115", "torch>=2.5,<3"]\n',
        )
        assert len(check_runtime_dependencies(path)) == 1

    def test_extras_and_dev_groups_are_exempt(self, tmp_path: Path) -> None:
        # training/requirements are meant to carry torch. Only the runtime list is closed.
        path = write(
            tmp_path,
            "pyproject.toml",
            '[project]\nname = "x"\ndependencies = ["fastapi"]\n'
            '[project.optional-dependencies]\ntrain = ["torch>=2.5"]\n',
        )
        assert check_runtime_dependencies(path) == []
