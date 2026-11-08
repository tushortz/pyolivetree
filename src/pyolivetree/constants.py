"""Hosts, protocol values and signing keys for the Olive Tree APIs."""

from __future__ import annotations

from enum import Enum

#: Main site: store, account, legacy APIs, in-app message center.
WWW = "https://www.olivetree.com"
#: Store JSON API (catalog, library, purchases).
STORE = f"{WWW}/store/br5/app/json/store"
#: Account JSON API (login, tokens, subscriptions).
ACCOUNT = f"{WWW}/store/br5/app/json/account"
#: In-app XML API (product registration and download links).
XML = f"{WWW}/store/br5/app/in-app/xml"
#: Sync server for notes, highlights, library and reading-plan data.
SYNC = "https://sync.olivetree.com"
#: Smart Search AI.
AI_API = "https://biblesearch-ai.olivetree.com/api/v1"
#: Smart Search AI staging host (serves the model list).
AI_STAGING_API = "https://staging-biblesearch-ai.olivetree.com/api/v1"
#: Event analytics and A/B experiments.
ANALYTICS = "https://analytics.olivetree.com/api/v1"
#: Consent, privacy and session telemetry.
PRIVACY = "https://privacy.olivetree.com/api/v1"
#: Text-to-speech for audio reading plans.
SPEECH = "https://speech.olivetree.com/api"
#: Static images (covers, reading-plan art).
CDN = "https://cdn.olivetree.com"
#: Legacy product images.
MEDIA = "https://media.olivetree.com"
#: Verse-of-the-day images.
VOTD = "https://votd.olivetree.com"
#: Help center.
HELP = "https://help.olivetree.com"
#: Firebase Realtime Database.
FIREBASE = "https://biblereader-android-df00f.firebaseio.com"

#: Sync protocol version for token-based accounts (4 otherwise).
SYNC_PROTOCOL = 6
#: Client platform id.
PLATFORM_ID = 26
#: Server ``errorCode`` values that mean the token is missing or expired.
TOKEN_ERRORS = frozenset({1018, 1020})


class DataSet(str, Enum):
    """Sync data sets. Every method that takes a data set accepts a member or its string value.

    Members are strings, so ``DataSet.ANNOTATIONS == "annotations"``.
    """

    #: Notes, highlights, clips, categories and highlighters.
    ANNOTATIONS = "annotations"
    #: Library categories, document details and last-read locations.
    LIBRARY = "library"
    #: Reading plans and their progress.
    DAILY_READING = "daily_reading"
    #: Recently opened text and audio locations.
    BOOKSHELF = "bookshelf"

    def __str__(self) -> str:
        return self.value


#: All data sets, in backup order.
DATA_SETS = tuple(DataSet)


def data_set_name(data_set: DataSet | str) -> str:
    """Return the plain name of a data set.

    Args:
        data_set: A :class:`DataSet`, its value (``"annotations"``), or the server form
            (``"managed_annotations"``). Other strings pass through unchanged.

    Returns:
        e.g. ``"annotations"``.
    """
    name = data_set.value if isinstance(data_set, DataSet) else str(data_set)
    return name.removeprefix("managed_")


#: HMAC-SHA512 client keys for signed endpoints, by service.
HMAC_KEYS = {
    "telemetry": bytes.fromhex(
        "483136e789e9781c4bf4b94a405da7b4c3109a559d1429883e71eb032cfcdc9"
        "ceb3f76381639321b4890449ac0093c3c103e9b4b19e213d3c34f02dc4106a87e"
    ),
    "ai": bytes.fromhex(
        "c69b54518884da105554f4dda9ac30b16d14f1d084318bbc389f00debaa0f37c"
        "3f29b7494afdbe41abb7eab9c7eb5bb234cb02b2f9355cc8997c105756d580a6"
    ),
    "consent": bytes.fromhex(
        "f91c94eb56d2e0ae31b902828b931243b5a0956c8f99a4ace778655d39f65511"
        "f4f6123046516609630241a879d705c6f02b3d197bbbe78e16265eeaac87f875"
    ),
    "features": bytes.fromhex(
        "d11bde62682b4b41253c4f6eec12d2a0095aa1802f92343e703af16a29168617"
        "081c6859384f960d7680989c0600ba596e2a5d17d0444424fdd4b367ce75402b"
    ),
}
