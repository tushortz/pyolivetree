"""Command line: ``pyolivetree backup|notes|highlights|clips|status|library``."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pyolivetree.client import OliveTree
from pyolivetree.exceptions import OliveTreeError
from pyolivetree.notes import to_markdown

COMMANDS = ("backup", "notes", "highlights", "clips", "status", "library")


def main(argv: list[str] | None = None) -> None:
    """Run the command line. ``argv`` defaults to ``sys.argv[1:]``.

    ``notes``, ``highlights`` and ``clips`` print Markdown from the local backup (add ``--refresh``
    to sync first). ``backup``, ``status`` and ``library`` print JSON.
    """
    p = argparse.ArgumentParser(prog="pyolivetree", description="Back up and export your Olive Tree notes.")
    p.add_argument("command", choices=COMMANDS)
    p.add_argument("--db", default="olivetree.db", help="local backup file (default: olivetree.db)")
    p.add_argument("--out", help="write output to this file instead of stdout")
    p.add_argument("--refresh", action="store_true", help="sync changes before exporting")
    a = p.parse_args(argv)

    try:
        text = _run(a)
    except OliveTreeError as e:
        p.exit(1, f"pyolivetree: error: {e}\n")
    Path(a.out).write_text(text) if a.out else print(text)


def _run(a: argparse.Namespace) -> str:
    with OliveTree() as ot:
        if a.command in ("notes", "highlights", "clips"):
            return to_markdown(getattr(ot, a.command)(a.db, refresh=a.refresh))
        if a.command == "backup":
            return json.dumps(ot.backup(a.db), indent=2)
        return json.dumps(getattr(ot, a.command)(), indent=2)
