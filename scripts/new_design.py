"""Create a design doc from docs/design/_template.md and add it to the index.

Documentation helper, not part of the service:

    uv run python scripts/new_design.py "passport creation flow"

Design docs are written before implementation; see CLAUDE.md §1.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN_DIR = ROOT / "docs" / "design"
TEMPLATE = DESIGN_DIR / "_template.md"
INDEX = DESIGN_DIR / "README.md"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def append_index_row(title: str, filename: str) -> None:
    if not INDEX.exists():
        return
    lines = INDEX.read_text(encoding="utf-8").splitlines()
    rows = [i for i, line in enumerate(lines) if line.startswith("|")]
    row = f"| {title} | draft | `{filename}` |"
    if not rows:
        lines += ["", "| Feature | Status | Doc |", "|---|---|---|", row]
    else:
        last = rows[-1]
        # Replace the "none yet" placeholder row the index starts with, if it is still there.
        if "none yet" in lines[last]:
            lines[last] = row
        else:
            lines.insert(last + 1, row)
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("title", nargs="+", help="feature name")
    args = parser.parse_args(argv)
    title = " ".join(args.title).strip()

    if not TEMPLATE.exists():
        print(f"template missing: {TEMPLATE}", file=sys.stderr)
        return 1

    filename = f"{slugify(title)}.md"
    target = DESIGN_DIR / filename
    if target.exists():
        print(f"already exists: {target}", file=sys.stderr)
        return 1

    today = dt.date.today().isoformat()
    text = TEMPLATE.read_text(encoding="utf-8")
    text = re.sub(r"^# Design: .*$", f"# Design: {title}", text, count=1, flags=re.M)
    text = re.sub(r"^- \*\*Status:\*\* .*$", "- **Status:** draft", text, count=1, flags=re.M)
    text = re.sub(r"^- \*\*Date:\*\* .*$", f"- **Date:** {today}", text, count=1, flags=re.M)
    target.write_text(text, encoding="utf-8")
    append_index_row(title, filename)
    print(f"created {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
