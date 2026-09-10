#!/usr/bin/env python3
"""Fetch, pin and verify the Catena-X aspect models this project binds to.

The aspect models are the schema of record. They live upstream in
``eclipse-tractusx/sldt-semantic-models``, they are versioned, and they change —
BatteryPass alone has shipped six major versions. Two failure modes follow from that,
and both are silent.

The first is drift: a build that fetches from a branch produces different bindings on
different days, and nothing says so. Every model here is therefore pinned to a commit
hash rather than a tag or a branch. A tag can be moved. A commit cannot.

The second is substitution: a file that arrives corrupted, truncated, or from a
mirror that is not what it claims to be. Every file is hashed on first fetch and
recorded in a manifest beside it, and ``--check`` re-verifies without touching the
network. CI runs ``--check``, so a modified aspect model fails the build rather than
quietly changing what "conformant" means.

Note which version is pinned for the imported model. BatteryPass 6.1.0 imports
DigitalProductPassport **5.0.0**, while the upstream repository has since published
7.0.0. Following "latest" would break the import. This is the whole argument for
pinning, in one example.

Usage
-----
    python scripts/fetch_samm.py            # fetch anything missing, verify the rest
    python scripts/fetch_samm.py --check    # verify only, never download; CI uses this
    python scripts/fetch_samm.py --force    # re-download even if hashes match
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
SOURCES = REPO / "samm-models" / "sources.json"
RAW = "https://raw.githubusercontent.com"
TIMEOUT_SECONDS = 60


class FetchError(RuntimeError):
    """Anything that should stop the run with a message rather than a traceback."""


@dataclass(frozen=True)
class Model:
    namespace: str
    version: str
    commit: str
    aspect: str
    files: tuple[str, ...]
    repository: str

    @property
    def urn(self) -> str:
        """The semantic URN the Turtle itself uses for this model's default prefix."""
        return f"urn:samm:{self.namespace}:{self.version}"

    @property
    def directory(self) -> Path:
        return REPO / "samm-models" / self.namespace / self.version

    def url(self, relative: str) -> str:
        return f"{RAW}/{self.repository}/{self.commit}/{self.namespace}/{self.version}/{relative}"


def load_models(sources: Path) -> list[Model]:
    data: dict[str, Any] = json.loads(sources.read_text(encoding="utf-8"))
    repository = data["repository"]
    models = []
    for entry in data["models"]:
        commit = entry["commit"]
        # A short hash would still resolve on GitHub, and would still be ambiguous.
        if len(commit) != 40 or not all(c in "0123456789abcdef" for c in commit):
            raise FetchError(
                f"{entry['namespace']} {entry['version']}: commit must be a full 40-character "
                f"hash, got {commit!r}. A branch or tag name is not a pin."
            )
        models.append(
            Model(
                namespace=entry["namespace"],
                version=entry["version"],
                commit=commit,
                aspect=entry["aspect"],
                files=tuple(entry["files"]),
                repository=repository,
            )
        )
    return models


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "batteriepass-fetch-samm"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return bytes(response.read())
    except urllib.error.HTTPError as exc:
        raise FetchError(f"{url}: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise FetchError(f"{url}: {exc.reason}") from exc


def read_manifest(model: Model) -> dict[str, Any] | None:
    path = model.directory / "manifest.json"
    if not path.is_file():
        return None
    manifest: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return manifest


def write_manifest(model: Model, hashes: dict[str, str]) -> None:
    manifest = {
        "namespace": model.namespace,
        "version": model.version,
        "urn": model.urn,
        "aspect": model.aspect,
        "repository": model.repository,
        "commit": model.commit,
        "license": "CC-BY-4.0",
        "files": dict(sorted(hashes.items())),
    }
    path = model.directory / "manifest.json"
    # sort_keys and a trailing newline so a re-fetch of unchanged files is a no-op diff.
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify(model: Model) -> list[str]:
    """Return a list of problems. Empty means the pinned files on disk are intact."""
    manifest = read_manifest(model)
    if manifest is None:
        return [f"{model.namespace} {model.version}: no manifest; run without --check first"]

    problems: list[str] = []
    if manifest.get("commit") != model.commit:
        problems.append(
            f"{model.namespace} {model.version}: manifest pins commit "
            f"{manifest.get('commit')} but sources.json pins {model.commit}. "
            f"Re-fetch to adopt the new pin — this is a deliberate change, not a repair."
        )

    recorded: dict[str, str] = manifest.get("files", {})
    for relative in model.files:
        path = model.directory / relative
        if not path.is_file():
            problems.append(f"{path.relative_to(REPO)}: missing")
            continue
        if relative not in recorded:
            problems.append(f"{path.relative_to(REPO)}: present but not in the manifest")
            continue
        actual = sha256(path.read_bytes())
        if actual != recorded[relative]:
            problems.append(
                f"{path.relative_to(REPO)}: hash mismatch\n"
                f"      expected {recorded[relative]}\n"
                f"      actual   {actual}"
            )

    for orphan in sorted(set(recorded) - set(model.files)):
        problems.append(
            f"{model.namespace} {model.version}: manifest records {orphan}, "
            f"which sources.json no longer lists"
        )
    return problems


def fetch(model: Model, *, force: bool) -> bool:
    """Fetch anything missing or changed. Return True if the tree was written to."""
    manifest = read_manifest(model)
    recorded: dict[str, str] = {} if manifest is None else manifest.get("files", {})
    pin_changed = manifest is not None and manifest.get("commit") != model.commit

    hashes: dict[str, str] = {}
    changed = False

    for relative in model.files:
        path = model.directory / relative
        if not force and not pin_changed and path.is_file() and relative in recorded:
            actual = sha256(path.read_bytes())
            if actual == recorded[relative]:
                hashes[relative] = actual
                continue

        print(f"  fetching {model.namespace}/{model.version}/{relative}")
        payload = download(model.url(relative))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        hashes[relative] = sha256(payload)
        changed = True

    if changed or manifest is None or pin_changed or recorded != hashes:
        write_manifest(model, hashes)
        changed = True
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify hashes against the manifests and exit; never downloads",
    )
    parser.add_argument(
        "--force", action="store_true", help="re-download even when hashes already match"
    )
    parser.add_argument("--sources", type=Path, default=SOURCES)
    args = parser.parse_args(argv)

    try:
        models = load_models(args.sources)
    except FetchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        problems = [problem for model in models for problem in verify(model)]
        if problems:
            print("Pinned aspect models do not match their manifests:\n", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)
            print(
                "\nThe aspect models are the schema of record. If this changed on purpose, "
                "update sources.json and re-run without --check, and expect the generated "
                "bindings to change with it.",
                file=sys.stderr,
            )
            return 1
        total = sum(len(m.files) for m in models)
        print(f"Verified {total} pinned files across {len(models)} aspect models.")
        return 0

    try:
        touched = [model for model in models if fetch(model, force=args.force)]
    except FetchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if touched:
        print(f"Updated {len(touched)} of {len(models)} aspect models.")
    else:
        print(f"All {len(models)} aspect models already pinned and intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
