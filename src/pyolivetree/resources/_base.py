"""Base class shared by every resource group."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyolivetree.client import OliveTree


class Resource:
    """A group of related endpoints bound to one :class:`~pyolivetree.OliveTree` client."""

    def __init__(self, client: OliveTree) -> None:
        self._c = client


def ids(product_ids: tuple[int, ...]) -> str:
    """Join ids the way the API expects in paths: ``"1,2,3"``."""
    return ",".join(map(str, product_ids))
