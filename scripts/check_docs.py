"""Fail when source changed but the documentation did not.

Documentation guard, run in CI (.github/workflows/docs-check.yml) and locally:

    uv run python scripts/check_docs.py            # compares HEAD against origin/main
    uv run python scripts/check_docs.py main       # or any base ref

The contract is in CLAUDE.md §1 and §6: a change under src/, training/, profiles/ or
scripts/ must come with a change under docs/ (a design doc, an ADR, ARCHITECTURE.md,
glossary.md or LEARNINGS.md), or the PR carries the `no-docs-needed` label, which the
workflow passes through as SKIP_DOCS_CHECK=1. Changed design docs and ADRs are also
checked for the sections the templates require. Standard library only.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories whose changes count as "source". Documentation helpers in scripts/ count
# too: a new guard or fetcher is a decision worth a sentence somewhere under docs/.
SOURCE = re.compile(r"^(src|training|profiles|scripts)/")
DOCS = re.compile(r"^docs/")
SKIP_NAMES = {"_template.md", "0000-template.md", "README.md"}


def changed_files(base: str) -> list[str]:
    """Files changed between the merge base with `base` and HEAD."""
    attempts = (
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        ["git", "diff", "--name-only", base, "HEAD"],
    )
    for args in attempts:
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    print(f"could not diff against {base!r}: {result.stderr.strip()}", file=sys.stderr)
    sys.exit(2)


def check_design_doc(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems = []
    if "```mermaid" not in text:
        problems.append("no Mermaid diagram (design docs need at least one)")
    if not re.search(r"^## .*scale review", text, flags=re.I | re.M):
        problems.append("missing 'Scale review' section")
    if not re.search(r"^## .*test plan", text, flags=re.I | re.M):
        problems.append("missing 'Test plan' section")
    return problems


def check_adr(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    required = ("Context", "Decision", "Consequences")
    problems = [f"missing '## {h}'" for h in required if f"## {h}" not in text]
    if "rejected" not in text.lower():
        problems.append("does not name the rejected alternative (required by docs/adr/README.md)")
    return problems


def main(argv: list[str]) -> int:
    if os.environ.get("SKIP_DOCS_CHECK") == "1":
        print("docs check skipped (SKIP_DOCS_CHECK=1)")
        return 0

    base = argv[1] if len(argv) > 1 else "origin/main"
    changed = changed_files(base)
    source_changed = [f for f in changed if SOURCE.match(f)]
    docs_changed = [f for f in changed if DOCS.match(f)]

    if source_changed and not docs_changed:
        print("Source changed but nothing under docs/ was touched.\n")
        print("Changed source files:")
        for f in source_changed:
            print(f"  {f}")
        print(
            "\nAdd or update a design doc, an ADR, docs/ARCHITECTURE.md, docs/glossary.md or "
            "docs/LEARNINGS.md, or label the PR 'no-docs-needed' with a one-line reason."
        )
        return 1

    status = 0
    for f in docs_changed:
        path = ROOT / f
        if not path.exists() or path.name in SKIP_NAMES:
            continue
        if f.startswith("docs/design/"):
            problems = check_design_doc(path)
        elif f.startswith("docs/adr/"):
            problems = check_adr(path)
        else:
            continue
        for p in problems:
            print(f"{f}: {p}")
            status = 1

    if status == 0:
        print("docs check passed")
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
