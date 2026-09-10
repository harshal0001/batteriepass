"""Load and verify an Annex XIII rule set.

The rule set is data, never constants. Both the regulation and the aspect model it is
mapped onto will move: six of the eight harmonised standards supporting Annex XIII
were adopted only in July 2026, and the EU digital product passport registry has been
operational since July 2026. A hard-coded attribute list would make every amendment a
code change, and would leave a stored passport unable to say which reading of the
rules it was judged against.

Every rule separates what the regulation says from what this project decided. The
identifier, verbatim text, access level and scope are parsed from the regulation and
hashed. The cluster, the passport paths and the dynamic flag are an editorial reading:
Annex XIII organises itself by who may read the information, not by subject, so the
seven reporting clusters are imposed on top of it.

``Rule.text_digest`` is what makes an amendment visible. It is recomputed on load and
compared against the digest recorded when the mapping was made, so text that changed
upstream un-reviews its own rule rather than silently keeping a stale mapping.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from bpass.core import Cluster

DEFAULT_ROOT = Path(__file__).resolve().parents[3] / "rulesets" / "annex-xiii"


class RulesetError(Exception):
    """A rule set that cannot be trusted to judge a passport."""


def text_digest(text: str) -> str:
    """Digest of regulation text, whitespace-collapsed and case-folded.

    Collapsed so a reflow in the published markup does not read as an amendment, and
    case-folded for the same reason. Anything surviving both is a real change.
    """
    normalised = re.sub(r"\s+", " ", text).strip().casefold()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class Rule:
    """One mandatory point of Annex XIII, and where it lives in the passport."""

    id: str
    part: int
    point: str
    text: str
    access: str
    scope: str
    cluster: Cluster
    paths: tuple[str, ...]
    dynamic: bool
    max_age_days: int | None = None
    note: str = ""

    @property
    def mapped(self) -> bool:
        """Whether any passport path satisfies this point.

        A mandatory point with no path is reported rather than dropped. BatteryPass
        6.1.0 models nothing for point 2(b), and a coverage report that omitted it
        would overstate conformance by one attribute.
        """
        return bool(self.paths)


@dataclass(frozen=True)
class Ruleset:
    version: str
    sha256: str
    rules: tuple[Rule, ...]

    def by_cluster(self, cluster: Cluster) -> tuple[Rule, ...]:
        return tuple(rule for rule in self.rules if rule.cluster == cluster)

    @property
    def dynamic_rules(self) -> tuple[Rule, ...]:
        return tuple(rule for rule in self.rules if rule.dynamic)

    @property
    def unmapped_rules(self) -> tuple[Rule, ...]:
        return tuple(rule for rule in self.rules if not rule.mapped)

    @property
    def paths(self) -> tuple[str, ...]:
        seen: list[str] = []
        for rule in self.rules:
            seen.extend(path for path in rule.paths if path not in seen)
        return tuple(seen)


def available_versions(root: Path = DEFAULT_ROOT) -> tuple[str, ...]:
    if not root.is_dir():
        return ()
    return tuple(sorted(p.name for p in root.iterdir() if (p / "ruleset.json").is_file()))


def _verify_files(directory: Path) -> str:
    """Check every file against the manifest. Return the rule set file's hash."""
    manifest_path = directory / "manifest.json"
    if not manifest_path.is_file():
        raise RulesetError(f"{directory.name}: no manifest. Run scripts/fetch_annex_xiii.py.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative, expected in manifest["files"].items():
        path = directory / relative
        if not path.is_file():
            raise RulesetError(f"{path}: recorded in the manifest but missing")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise RulesetError(
                f"{path}: hash mismatch against the manifest. Refusing to judge a "
                f"passport against a rule set that is not the one that was reviewed."
            )
    return str(manifest["files"]["ruleset.json"])


@lru_cache(maxsize=8)
def load(version: str, root: Path = DEFAULT_ROOT) -> Ruleset:
    """Load one version. Cached: the rule set is immutable and read on every request."""
    directory = root / version
    if not (directory / "ruleset.json").is_file():
        available = ", ".join(available_versions(root)) or "none"
        raise RulesetError(f"unknown rule set version {version!r}. Available: {available}")

    sha256 = _verify_files(directory)
    data = json.loads((directory / "ruleset.json").read_text(encoding="utf-8"))

    if data["version"] != version:
        raise RulesetError(
            f"{directory.name}: file declares version {data['version']!r}, "
            f"but it is stored under {version!r}"
        )

    rules = []
    for entry in data["rules"]:
        recorded = entry["text_digest"]
        actual = text_digest(entry["text"])
        if recorded != actual:
            raise RulesetError(
                f"{entry['id']}: regulation text does not match its recorded digest "
                f"({recorded} vs {actual}). The text was amended after the mapping was "
                f"made; the rule needs re-review before it can be used."
            )
        rules.append(
            Rule(
                id=entry["id"],
                part=entry["part"],
                point=entry["point"],
                text=entry["text"],
                access=entry["access"],
                scope=entry["scope"],
                cluster=Cluster(entry["cluster"]),
                paths=tuple(entry["paths"]),
                dynamic=entry["dynamic"],
                max_age_days=entry.get("max_age_days"),
                note=entry.get("note", ""),
            )
        )

    identifiers = [rule.id for rule in rules]
    if len(identifiers) != len(set(identifiers)):
        raise RulesetError(f"{version}: duplicate rule identifiers")

    return Ruleset(version=version, sha256=sha256, rules=tuple(rules))


def latest(root: Path = DEFAULT_ROOT) -> Ruleset:
    """The newest version by name. Versions are dates, so name order is date order."""
    versions = available_versions(root)
    if not versions:
        raise RulesetError(f"no rule sets found under {root}")
    return load(versions[-1], root)
