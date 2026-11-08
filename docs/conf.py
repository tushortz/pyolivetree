"""Sphinx configuration for pyolivetree."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

project = "pyolivetree"
author = "pyolivetree contributors"
copyright = "2026, pyolivetree contributors"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]

suppress_warnings = ["ref.python"]

autodoc_member_order = "bysource"
napoleon_google_docstring = True
typehints_defaults = "comma"
