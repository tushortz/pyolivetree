"""Command line: ``pyolivetree backup|notes|highlights|clips|status|library``."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pyolivetree.client import OliveTree
from pyolivetree.notes import annotations, backup, to_markdown


def main(argv: list[str] | None = None) -> None:
    """Run the command line. ``argv`` defaults to ``sys.argv[1:]``."""
    p = argparse.ArgumentParser(prog="pyolivetree", description="Back up and export your Olive Tree notes.")
    p.add_argument(
        "command",
        choices=["backup", "notes", "highlights", "clips", "status", "library"],
    )
    p.add_argument("--db", default="olivetree.db")
    p.add_argument("--out", help="write output to this file instead of stdout")
    a = p.parse_args(argv)

    if a.command in ("notes", "highlights", "clips"):
        text = to_markdown(annotations(a.db, a.command.rstrip("s")))
    else:
        with OliveTree() as ot:
            result = {
                "backup": lambda: backup(ot, a.db),
                "status": ot.sync.status,
                "library": ot.store.purchased,
            }[a.command]()
        text = json.dumps(result, indent=2)
    Path(a.out).write_text(text) if a.out else print(text)
