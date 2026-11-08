"""Python client for the Olive Tree Bible.

Example:
    >>> from pyolivetree import OliveTree       # doctest: +SKIP
    >>> with OliveTree() as ot:
    ...     ot.sync.status()
"""

from importlib.metadata import PackageNotFoundError, version

from pyolivetree._http import sign_body
from pyolivetree.async_client import AsyncOliveTree, AsyncOliveTreeClient
from pyolivetree.client import OliveTree, OliveTreeClient
from pyolivetree.constants import DataSet
from pyolivetree.exceptions import OliveTreeAPIError, OliveTreeAuthError, OliveTreeError
from pyolivetree.notes import annotations, backup, to_markdown, verse_ref

try:
    __version__ = version("pyolivetree")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0.0.0"

__all__ = [
    "AsyncOliveTree",
    "AsyncOliveTreeClient",
    "DataSet",
    "OliveTree",
    "OliveTreeAPIError",
    "OliveTreeAuthError",
    "OliveTreeClient",
    "OliveTreeError",
    "annotations",
    "backup",
    "sign_body",
    "to_markdown",
    "verse_ref",
]
