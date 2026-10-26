"""Create the next numbered ADR from docs/adr/0000-template.md and add it to the index.

Documentation helper, not part of the service. Lives in scripts/ so it runs with the rest
of the tooling:

    uv run python scripts/new_adr.py "Serve public pages from an edge cache"

The project's ADR style is fixed in docs/adr/README.md; this script only fills in the
number, title and date and appends an index row. It never touches an existing record.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADR_DIR = ROOT / "docs" / "adr"
TEMPLATE = ADR_DIR / "0000-template.md"
INDEX = ADR_DIR / "README.md"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def next_number() -> int:
    numbers = [
        int(p.name[:4])
        for p in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")
        if p.name[:4].isdigit() and p.name != TEMPLATE.name
    ]
    return max(numbers, default=0) + 1


def append_index_row(number: str, title: str, filename: str) -> None:
    """Insert a row after the last table row of the index, keeping trailing prose."""
    if not INDEX.exists():
        return
    lines = INDEX.read_text(encoding="utf-8").splitlines()
    last_row = max((i for i, line in enumerate(lines) if line.startswith("|")), default=None)
    row = f"| [{number}]({filename}) | {title} | Proposed |"
    if last_row is None:
        lines += ["", "| # | Decision | Status |", "|---|---|---|", row]
    else:
        lines.insert(last_row + 1, row)
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("title", nargs="+", help="decision title, stated as the decision")
    args = parser.parse_args(argv)
    title = " ".join(args.title).strip()

    if not TEMPLATE.exists():
        print(f"template missing: {TEMPLATE}", file=sys.stderr)
        return 1

    number = f"{next_number():04d}"
    filename = f"{number}-{slugify(title)}.md"
    target = ADR_DIR / filename
    if target.exists():
        print(f"already exists: {target}", file=sys.stderr)
        return 1

    today = dt.date.today().isoformat()
    text = TEMPLATE.read_text(encoding="utf-8")
    text = re.sub(r"^# NNNN — .*$", f"# {number} — {title}", text, count=1, flags=re.M)
    text = re.sub(
        r"^\*\*Status:\*\* .*$",
        f"**Status:** Proposed · **Date:** {today}",
        text,
        count=1,
        flags=re.M,
    )
    target.write_text(text, encoding="utf-8")
    append_index_row(number, title, filename)
    print(f"created {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
