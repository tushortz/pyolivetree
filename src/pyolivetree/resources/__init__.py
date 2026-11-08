"""Endpoint groups. Each is attached to :class:`~pyolivetree.OliveTree` as an attribute."""

from pyolivetree.resources.account import Account
from pyolivetree.resources.ai import AI
from pyolivetree.resources.firebase import Firebase
from pyolivetree.resources.media import Media
from pyolivetree.resources.messages import Messages
from pyolivetree.resources.products import Products
from pyolivetree.resources.reading import Reading
from pyolivetree.resources.store import Store
from pyolivetree.resources.sync import Sync
from pyolivetree.resources.telemetry import Telemetry
from pyolivetree.resources.web import Web

__all__ = [
    "AI",
    "Account",
    "Firebase",
    "Media",
    "Messages",
    "Products",
    "Reading",
    "Store",
    "Sync",
    "Telemetry",
    "Web",
]
