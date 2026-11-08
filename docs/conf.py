"""Sphinx configuration."""

import os
import sys
from importlib.metadata import version as _version

sys.path.insert(0, os.path.abspath("../src"))

project = "pyolivetree"
author = "Taiwo Kareem"
copyright = "2026, Taiwo Kareem"
try:
    release = _version("pyolivetree")
except Exception:
    release = "2.0.0"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {"members": True, "show-inheritance": False}
napoleon_google_docstring = True
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
nitpicky = False

html_theme = "furo"
html_title = f"pyolivetree {release}"
html_static_path = ["_static"]
exclude_patterns = ["_build"]
