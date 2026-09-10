#!/usr/bin/env python3
"""Fetch Annex XIII of Regulation (EU) 2023/1542 from EUR-Lex and pin it.

The conformance engine checks a passport against the attributes Annex XIII mandates.
That list is the authority, so it is treated the way the aspect models are: fetched
from the official source, extracted verbatim, hashed, and committed as data.

Typing the list from memory would have been faster and would have been wrong. The
first extraction against the real text corrected five points that the Catena-X aspect
model does not cite explicitly, and confirmed that Part 1 ends at (s) rather than
running to (t).

**Consolidated, not original.** The URL fetches the consolidated text, which
incorporates the corrigenda. Point 1(q) carries a ``C4`` marker in the consolidated
version: the original Official Journal text of that point was corrected. Checking
against the uncorrected original would encode a superseded requirement.

Usage
-----
    python scripts/fetch_annex_xiii.py --version 2025-07-31
    python scripts/fetch_annex_xiii.py --check      # verify offline; CI uses this
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULESETS = REPO / "rulesets" / "annex-xiii"

CELEX = "02023R1542-20250731"
SOURCE_URL = f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{CELEX}"
TIMEOUT_SECONDS = 180


class FetchError(RuntimeError):
    """Stop with a message rather than a traceback."""


def extract_annex(document: str) -> str:
    """Pull ANNEX XIII out of the full regulation, verbatim.

    EUR-Lex serves one HTML document of roughly 700 KB. Tags are stripped rather than
    parsed: the annex is a flat sequence of block elements, so the tag structure
    carries no information the text does not, and a dependency on an HTML parser would
    buy nothing.
    """
    text = html.unescape(re.sub(r"<[^>]+>", "\n", document))
    lines = [line.strip() for line in re.sub(r"[ \t]+", " ", text).split("\n")]
    lines = [line for line in lines if line]

    try:
        start = next(i for i, line in enumerate(lines) if line == "ANNEX XIII")
    except StopIteration:
        raise FetchError(
            "ANNEX XIII heading not found. EUR-Lex may have changed its markup, or the "
            "document was truncated in transit."
        ) from None
    try:
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("ANNEX XIV"))
    except StopIteration:
        raise FetchError("ANNEX XIV heading not found; refusing to guess where XIII ends") from None

    annex = lines[start:end]
    if len(annex) < 50:
        raise FetchError(f"extracted only {len(annex)} lines; expected the full annex")
    return "\n".join(annex) + "\n"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "batteriepass-fetch-annex"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return bytes(response.read()).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raise FetchError(f"{url}: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise FetchError(f"{url}: {exc.reason}") from exc


def verify(directory: Path) -> list[str]:
    manifest_path = directory / "manifest.json"
    if not manifest_path.is_file():
        return [f"{directory.name}: no manifest"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    problems: list[str] = []
    for relative, expected in manifest["files"].items():
        path = directory / relative
        if not path.is_file():
            problems.append(f"{path.relative_to(REPO)}: missing")
            continue
        actual = sha256(path.read_bytes())
        if actual != expected:
            problems.append(
                f"{path.relative_to(REPO)}: hash mismatch\n"
                f"      expected {expected}\n      actual   {actual}"
            )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="2025-07-31", help="consolidation date of the text")
    parser.add_argument("--check", action="store_true", help="verify hashes offline; no network")
    args = parser.parse_args(argv)

    if args.check:
        directories = (
            sorted(p for p in RULESETS.iterdir() if p.is_dir()) if RULESETS.is_dir() else []
        )
        if not directories:
            print("error: no rule sets found under rulesets/annex-xiii", file=sys.stderr)
            return 1
        problems = [problem for directory in directories for problem in verify(directory)]
        if problems:
            print("Annex XIII rule sets do not match their manifests:\n", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)
            print(
                "\nThe regulation text is the authority for what a passport must carry. "
                "If it changed on purpose, re-fetch and expect every affected rule to "
                "need re-review.",
                file=sys.stderr,
            )
            return 1
        print(f"Verified {len(directories)} Annex XIII rule set(s).")
        return 0

    directory = RULESETS / args.version
    directory.mkdir(parents=True, exist_ok=True)

    try:
        annex = extract_annex(download(SOURCE_URL))
    except FetchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    destination = directory / "annex-xiii.txt"
    previous = destination.read_bytes() if destination.is_file() else None
    payload = annex.encode("utf-8")
    destination.write_bytes(payload)

    manifest_path = directory / "manifest.json"
    existing = (
        json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    )
    files = dict(existing.get("files", {}))
    files["annex-xiii.txt"] = sha256(payload)
    if (directory / "ruleset.json").is_file():
        files["ruleset.json"] = sha256((directory / "ruleset.json").read_bytes())

    manifest_path.write_text(
        json.dumps(
            {
                "version": args.version,
                "regulation": "Regulation (EU) 2023/1542",
                "annex": "XIII",
                "celex": CELEX,
                "source": SOURCE_URL,
                "consolidated": True,
                "fetched_at": datetime.now(UTC).date().isoformat(),
                "files": dict(sorted(files.items())),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    if previous is not None and previous != payload:
        print(f"WARNING: {destination.name} CHANGED. Every rule mapped to it needs re-review.")
    print(f"wrote {destination.relative_to(REPO)} ({len(annex.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
