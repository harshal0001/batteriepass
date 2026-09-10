"""Regenerate the committed bindings.

    python -m bpass.samm.generate            # write the bindings
    python -m bpass.samm.generate --check    # fail if the committed output is stale

``--check`` is what CI runs. Generated code that is committed but not verified drifts
the moment someone edits it by hand or bumps a pin without regenerating, and the drift
is invisible until a payload fails in production. Regenerating and diffing turns
"never hand-edit this" from a comment into a build failure.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

from bpass.samm.emit import emit
from bpass.samm.loader import DEFAULT_ROOT, load_graph, load_sources
from bpass.samm.model import SammError
from bpass.samm.walk import resolve

BINDINGS = Path(__file__).resolve().parents[1] / "bindings"

# Which aspects get bindings. Everything else that is pinned is a dependency, loaded
# so references resolve but never emitted as a module of its own.
TARGETS: dict[str, str] = {
    "battery_pass": "urn:samm:io.catenax.battery.battery_pass:6.1.0#BatteryPass",
}


def render(target: str, root: Path = DEFAULT_ROOT) -> str:
    aspect_urn = TARGETS[target]
    graph, urns = load_graph(root)
    return emit(resolve(graph, aspect_urn, urns))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=sorted(TARGETS), action="append", dest="models")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed bindings match a fresh generation; write nothing",
    )
    parser.add_argument("--sources", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)

    targets = args.models or sorted(TARGETS)
    stale: list[str] = []

    for target in targets:
        destination = BINDINGS / f"{target}.py"
        try:
            generated = render(target, args.sources)
        except SammError as exc:
            print(f"error: {target}: {exc}", file=sys.stderr)
            return 1

        if args.check:
            if not destination.is_file():
                stale.append(f"{destination.name}: missing")
                continue
            committed = destination.read_text(encoding="utf-8")
            if committed != generated:
                diff = difflib.unified_diff(
                    committed.splitlines(),
                    generated.splitlines(),
                    fromfile=f"committed/{destination.name}",
                    tofile=f"generated/{destination.name}",
                    lineterm="",
                    n=1,
                )
                stale.append("\n".join(list(diff)[:40]))
            continue

        destination.write_text(generated, encoding="utf-8")
        lines = generated.count("\n")
        print(f"wrote {destination.relative_to(BINDINGS.parents[2])} ({lines} lines)")

    if args.check:
        if stale:
            print("Committed bindings are stale:\n", file=sys.stderr)
            for entry in stale:
                print(entry, file=sys.stderr)
            print(
                "\nRun `python -m bpass.samm.generate` and commit the result. Never edit "
                "the bindings by hand — the next regeneration would silently revert it.",
                file=sys.stderr,
            )
            return 1
        pinned = len(load_sources(args.sources))
        print(f"Bindings match a fresh generation from {pinned} pinned aspect models.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
