#!/usr/bin/env python3
"""Fail if the serving code could ever pull in PyTorch.

A CPU-only ``torch`` install is roughly 700 MB against ``onnxruntime``'s 50 MB. On
Lambda that difference is the cold start, and the cold start is whether a visitor
waits or closes the tab. Training therefore lives in ``training/`` and the only
artefact that crosses into ``src/`` is an ONNX file.

That boundary is one careless import away from collapsing, and nothing about a
green test suite would reveal it — the image would simply get slow. So it is
checked mechanically, in CI, on every pull request.

Two checks:

1. **Static imports.** Parse every module under ``src/`` with ``ast`` and reject any
   import of a banned package. Parsing rather than grepping means a docstring that
   mentions torch (this one does) is not a false positive, and ``import torch as t``
   is not a false negative.
2. **Runtime dependencies.** Reject a banned package in the runtime dependency list,
   which is the other way it could reach the image.

Exit code 0 if clean, 1 otherwise.
"""

from __future__ import annotations

import ast
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Torch and the ecosystem that drags it in. Anything here in the serving path means
# the image is about to grow by hundreds of megabytes.
BANNED = frozenset(
    {
        "torch",
        "torchvision",
        "torchaudio",
        "pytorch_lightning",
        "lightning",
        "transformers",
        "accelerate",
    }
)

# Directories that are allowed to import whatever they like, because they never
# ship. training/ is the point of the split; tests/ exercises exported artefacts.
EXEMPT = ("training", "tests")


def _top_level(module: str) -> str:
    return module.partition(".")[0]


def banned_imports(path: Path) -> list[tuple[int, str]]:
    """Return (line number, package) for every banned import in one module."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:  # a file that will not parse cannot be cleared
        print(f"{path}: cannot parse: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    hits: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _top_level(alias.name) in BANNED:
                    hits.append((node.lineno, _top_level(alias.name)))
        elif (
            isinstance(node, ast.ImportFrom)
            # A relative import (level > 0) has no top-level package to ban.
            and node.level == 0
            and node.module
            and _top_level(node.module) in BANNED
        ):
            hits.append((node.lineno, _top_level(node.module)))
    return hits


def check_sources(root: Path) -> list[str]:
    problems: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in EXEMPT for part in path.parts):
            continue
        for lineno, package in banned_imports(path):
            problems.append(f"{path.relative_to(REPO)}:{lineno} imports {package}")
    return problems


def check_runtime_dependencies(pyproject: Path) -> list[str]:
    """The runtime dependency list is what the image installs. Nothing banned in it.

    Optional extras and the dev group are exempt: they exist precisely so that
    generation, feature extraction and testing can use packages the image does not.
    """
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    problems: list[str] = []
    for spec in data.get("project", {}).get("dependencies", []):
        # "torch>=2.5,<3" -> "torch"; also handles extras and environment markers.
        name = spec.split(";")[0].split("[")[0].strip()
        for separator in (">=", "<=", "==", "!=", "~=", ">", "<"):
            name = name.split(separator)[0]
        if name.strip().replace("-", "_").lower() in BANNED:
            problems.append(f"pyproject.toml: runtime dependency {spec!r} is banned")
    return problems


def main() -> int:
    problems = check_sources(REPO / "src") + check_runtime_dependencies(REPO / "pyproject.toml")

    if problems:
        print("The serving boundary is broken:\n", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        print(
            "\nsrc/ and the runtime dependencies must stay free of torch. Move the code "
            "to training/, or export the model to ONNX and load it through "
            "bpass.inference instead.",
            file=sys.stderr,
        )
        return 1

    print("Serving boundary intact: no torch under src/ or in runtime dependencies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
