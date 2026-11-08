"""Every endpoint method: HTTP method, URL, auth and signing, plus key parameters."""

from __future__ import annotations

import json
from urllib.parse import parse_qs

import httpx
import pytest

from pyolivetree import sign_body
from pyolivetree.constants import (
    ACCOUNT,
    AI_API,
    AI_STAGING_API,
    ANALYTICS,
    CDN,
    FIREBASE,
    HELP,
    MEDIA,
    PRIVACY,
    SPEECH,
    STORE,
    SYNC,
    VOTD,
    WWW,
    XML,
)

MSG = f"{WWW}/api/messages/v1"

# (id, call, method, url without query, sends bearer token, HMAC profile)
ENDPOINTS = [
    # account
    (
        "account.access_token",
        lambda o: o.account.access_token(),
        "POST",
        f"{ACCOUNT}/access_token",
        False,
        None,
    ),
    (
        "account.signup",
        lambda o: o.account.signup("n@example.com", "pw2"),
        "POST",
        f"{ACCOUNT}/account_signup",
        False,
        None,
    ),
    (
        "account.forgot_password",
        lambda o: o.account.forgot_password("a@b.c"),
        "POST",
        f"{ACCOUNT}/forgot_password",
        False,
        None,
    ),
    (
        "account.web_handoff_token",
        lambda o: o.account.web_handoff_token(),
        "POST",
        f"{ACCOUNT}/generate_web_handoff_token",
        True,
        None,
    ),
    (
        "account.subscription",
        lambda o: o.account.subscription(5),
        "POST",
        f"{ACCOUNT}/subscription/5",
        True,
        None,
    ),
    (
        "account.add_variable_subscription_selections",
        lambda o: o.account.add_variable_subscription_selections(7),
        "POST",
        f"{ACCOUNT}/add_variable_subscription_selections/7",
        True,
        None,
    ),
    # store
    *[
        (f"store.{m}", lambda o, m=m: getattr(o.store, m)(), "POST", f"{STORE}/{p}", True, None)
        for m, p in [
            ("home", "home"),
            ("banner", "banner"),
            ("featured_categories", "featured_categories"),
            ("library", "library"),
            ("purchased", "purchased"),
            ("wishlists", "user_wishlists"),
            ("subscriptions_available", "subscriptions_available"),
            ("first_run_subscriptions", "first_run_subscriptions"),
            ("first_run_interests", "first_run_interests"),
            ("first_run_bible_list", "first_run_bible_list"),
            ("need_interests", "need_interests"),
            ("paid_features", "paid_features"),
            ("paid_features_marketing", "paid_features_marketing"),
            ("ads", "ads"),
            ("product_manifest", "product_manifest"),
            ("register_subscription", "register_subscription"),
            ("validate_google_in_app_purchase", "validate_google_in_app_purchase"),
            ("support_delete_account", "support_delete_account"),
        ]
    ],
    ("store.product", lambda o: o.store.product(36163), "POST", f"{STORE}/product/36163", True, None),
    ("store.products", lambda o: o.store.products(1, 2), "POST", f"{STORE}/product_set/1,2", True, None),
    ("store.category", lambda o: o.store.category(3), "POST", f"{STORE}/cat/3", True, None),
    (
        "store.library_details",
        lambda o: o.store.library_details(1, 2),
        "POST",
        f"{STORE}/library_details/1,2",
        True,
        None,
    ),
    ("store.giveaway", lambda o: o.store.giveaway("FREE"), "POST", f"{STORE}/giveaway/FREE", True, None),
    (
        "store.allow_subscription_purchase",
        lambda o: o.store.allow_subscription_purchase("plan"),
        "POST",
        f"{STORE}/allow_subscription_purchase/plan",
        True,
        None,
    ),
    (
        "store.subscription_variable_product_selection",
        lambda o: o.store.subscription_variable_product_selection(4),
        "POST",
        f"{STORE}/subscription_variable_product_selection/4",
        True,
        None,
    ),
    (
        "store.wishlist_add",
        lambda o: o.store.wishlist_add(1, 2),
        "POST",
        f"{STORE}/modify_wishlist/add",
        True,
        None,
    ),
    (
        "store.wishlist_remove",
        lambda o: o.store.wishlist_remove(1),
        "POST",
        f"{STORE}/modify_wishlist/remove",
        True,
        None,
    ),
    ("store.path", lambda o: o.store.path("/rc/section/9"), "POST", f"{STORE}/rc/section/9", True, None),
    ("store.search", lambda o: o.store.search("faith"), "POST", f"{STORE}/search", True, None),
    # products
    (
        "products.download_links",
        lambda o: o.products.download_links(1, 2),
        "POST",
        f"{XML}/download_products/1,2",
        True,
        None,
    ),
    ("products.register", lambda o: o.products.register(), "POST", f"{XML}/register_products", True, None),
    ("products.info", lambda o: o.products.info(), "POST", f"{XML}/product_info", True, None),
    (
        "products.updates",
        lambda o: o.products.updates({"a": 1}),
        "POST",
        f"{XML}/product_updates",
        False,
        None,
    ),
    (
        "products.email_signup",
        lambda o: o.products.email_signup("a@b.c"),
        "POST",
        f"{XML}/email_signup",
        True,
        None,
    ),
    (
        "products.reading_templates",
        lambda o: o.products.reading_templates(1, 2),
        "GET",
        f"{XML}/download_reading_templates",
        False,
        None,
    ),
    # sync
    ("sync.status", lambda o: o.sync.status(), "GET", f"{SYNC}/syncables/status.json", True, None),
    ("sync.page", lambda o: o.sync.page("library", 5), "GET", f"{SYNC}/syncables.json", True, None),
    (
        "sync.table_schema",
        lambda o: o.sync.table_schema("annotations", "highlighters", 2),
        "GET",
        f"{SYNC}/syncables/get_table_schema/managed_annotations/highlighters/2.json",
        True,
        None,
    ),
    (
        "sync.push",
        lambda o: o.sync.push("annotations", {"title": "t"}, customer_id=42),
        "POST",
        f"{SYNC}/syncables/syncitem.json",
        True,
        None,
    ),
    (
        "sync.release_lock",
        lambda o: o.sync.release_lock(),
        "PUT",
        f"{SYNC}/syncables/release_lock",
        True,
        None,
    ),
    (
        "sync.possibly_bad_annotation_data",
        lambda o: o.sync.possibly_bad_annotation_data(),
        "GET",
        f"{SYNC}/syncables/get_possibly_bad_annotation_data.json",
        True,
        None,
    ),
    # ai
    ("ai.query", lambda o: o.ai.query("patience"), "POST", f"{AI_API}/query", True, "ai"),
    ("ai.status", lambda o: o.ai.status(), "GET", f"{AI_API}/status", True, None),
    ("ai.set_usage", lambda o: o.ai.set_usage(5, 1, 10), "PUT", f"{AI_API}/set-my-usage", True, "ai"),
    ("ai.models", lambda o: o.ai.models(), "GET", f"{AI_STAGING_API}/models", False, None),
    # reading
    (
        "reading.daily_reading",
        lambda o: o.reading.daily_reading(),
        "GET",
        f"{WWW}/api/daily_reading_v2.php",
        False,
        None,
    ),
    (
        "reading.recommended",
        lambda o: o.reading.recommended(),
        "POST",
        f"{WWW}/api/recommended.php",
        False,
        None,
    ),
    (
        "reading.verse_of_the_day",
        lambda o: o.reading.verse_of_the_day("2026-11-08"),
        "GET",
        f"{WWW}/votd/index.php",
        False,
        None,
    ),
    (
        "reading.verse_of_the_day_image",
        lambda o: o.reading.verse_of_the_day_image(11, 8, 1),
        "GET",
        f"{VOTD}/11/8/1",
        False,
        None,
    ),
    (
        "reading.now_reading",
        lambda o: o.reading.now_reading("en", "plan/1"),
        "GET",
        f"{SPEECH}/nowreading/en/plan/1",
        False,
        None,
    ),
    (
        "reading.completed_message",
        lambda o: o.reading.completed_message(),
        "GET",
        f"{SPEECH}/messages/en/completed",
        False,
        None,
    ),
    # media
    ("media.cover", lambda o: o.media.cover(1), "GET", f"{CDN}/images/covers/1.jpg", False, None),
    (
        "media.cover_stack",
        lambda o: o.media.cover_stack(1),
        "GET",
        f"{CDN}/images/covers/1_stack.png",
        False,
        None,
    ),
    (
        "media.product_image",
        lambda o: o.media.product_image(1),
        "GET",
        f"{MEDIA}/store/images40/1.jpg",
        False,
        None,
    ),
    (
        "media.reading_plan_image",
        lambda o: o.media.reading_plan_image(5, "grid"),
        "GET",
        f"{CDN}/images/reading_plans/5_grid.jpg",
        False,
        None,
    ),
    (
        "media.reading_plan_list_image",
        lambda o: o.media.reading_plan_list_image(5),
        "GET",
        f"{WWW}/store/images/reading_plans/5_list.jpg",
        False,
        None,
    ),
    (
        "media.stream",
        lambda o: o.media.stream(1, "track"),
        "GET",
        f"{WWW}/media/content/1/track/stream.mpd",
        True,
        None,
    ),
    # messages
    ("messages.list", lambda o: o.messages.list(), "POST", f"{MSG}/messages.php", False, "telemetry"),
    (
        "messages.register_device",
        lambda o: o.messages.register_device(token="t"),
        "POST",
        f"{MSG}/devices.php",
        False,
        "telemetry",
    ),
    (
        "messages.metrics",
        lambda o: o.messages.metrics(3, {"seen": 1}),
        "POST",
        f"{MSG}/metrics.php",
        False,
        "telemetry",
    ),
    # telemetry
    (
        "telemetry.event_manifest",
        lambda o: o.telemetry.event_manifest(),
        "GET",
        f"{ANALYTICS}/event_manifest",
        False,
        None,
    ),
    (
        "telemetry.event_manifest[range]",
        lambda o: o.telemetry.event_manifest("2026-01-01", "2026-02-01"),
        "GET",
        f"{ANALYTICS}/event_manifests/from/2026-01-01/to/2026-02-01",
        False,
        None,
    ),
    (
        "telemetry.get_variant",
        lambda o: o.telemetry.get_variant("exp"),
        "GET",
        f"{ANALYTICS}/variant",
        False,
        None,
    ),
    (
        "telemetry.set_variant",
        lambda o: o.telemetry.set_variant(a=1),
        "PUT",
        f"{ANALYTICS}/variant",
        False,
        None,
    ),
    (
        "telemetry.events",
        lambda o: o.telemetry.events([{"e": 1}]),
        "POST",
        f"{ANALYTICS}/events",
        False,
        "telemetry",
    ),
    (
        "telemetry.session_start",
        lambda o: o.telemetry.session_start(a=1),
        "POST",
        f"{PRIVACY}/session/start",
        False,
        "telemetry",
    ),
    (
        "telemetry.consent_receipt",
        lambda o: o.telemetry.consent_receipt(a=1),
        "POST",
        f"{PRIVACY}/consent/receipt",
        False,
        None,
    ),
    (
        "telemetry.location_settings[get]",
        lambda o: o.telemetry.location_settings(),
        "GET",
        f"{PRIVACY}/consent/location/settings",
        False,
        None,
    ),
    (
        "telemetry.location_settings[set]",
        lambda o: o.telemetry.location_settings(a=1),
        "POST",
        f"{PRIVACY}/consent/location/settings",
        False,
        None,
    ),
    (
        "telemetry.subscription_log_usage",
        lambda o: o.telemetry.subscription_log_usage(a=1),
        "POST",
        f"{PRIVACY}/subscription/log_usage",
        False,
        None,
    ),
    # web
    (
        "web.timeouts",
        lambda o: o.web.timeouts(),
        "GET",
        f"{WWW}/static/app_assets/timeouts.json",
        False,
        None,
    ),
    (
        "web.appirater_config",
        lambda o: o.web.appirater_config(),
        "GET",
        f"{WWW}/api/appirater_config.json",
        False,
        None,
    ),
    (
        "web.app_to_web_bridge",
        lambda o: o.web.app_to_web_bridge(productid=1),
        "GET",
        f"{WWW}/store/br5/app_to_web_bridge.php",
        False,
        None,
    ),
    ("web.product_page", lambda o: o.web.product_page(1), "GET", f"{WWW}/store/product.php", False, None),
    (
        "web.bible_study_packs",
        lambda o: o.web.bible_study_packs(),
        "GET",
        f"{WWW}/store/biblestudypacks.php",
        False,
        None,
    ),
    (
        "web.manage_subscriptions",
        lambda o: o.web.manage_subscriptions(),
        "GET",
        f"{WWW}/store/manage_subscriptions.php",
        False,
        None,
    ),
    ("web.eula", lambda o: o.web.eula(), "GET", f"{WWW}/eula", False, None),
    ("web.privacy_policy", lambda o: o.web.privacy_policy(), "GET", f"{WWW}/privacy_policy", False, None),
    (
        "web.help_articles",
        lambda o: o.web.help_articles(),
        "GET",
        f"{HELP}/hc/en-us/sections/360000034263-Android-OLIVE-TREE-BIBLE-APP-7-1",
        False,
        None,
    ),
    (
        "web.help_login",
        lambda o: o.web.help_login(),
        "GET",
        f"{HELP}/hc/en-us/articles/210270643-Get-Started-Logging-In",
        False,
        None,
    ),
    # firebase
    ("firebase.root", lambda o: o.firebase.root(), "GET", f"{FIREBASE}/.json", False, None),
    (
        "firebase.get",
        lambda o: o.firebase.get("/config/app/"),
        "GET",
        f"{FIREBASE}/config/app.json",
        False,
        None,
    ),
]


@pytest.mark.parametrize(
    ("call", "method", "url", "bearer", "profile"), [e[1:] for e in ENDPOINTS], ids=[e[0] for e in ENDPOINTS]
)
def test_endpoint(ot, rec, call, method, url, bearer, profile):
    call(ot)
    req = rec.last
    assert req.method == method
    assert str(req.url.copy_with(query=None)) == url
    assert ("OTAuthorization" in req.headers) is bearer
    if profile:
        assert req.headers["signature"] == sign_body(req.content, profile)
    else:
        assert "signature" not in req.headers


def test_every_public_method_is_covered(ot):
    covered = {e[0].split("[")[0] for e in ENDPOINTS}
    covered |= {
        "account.login",
        "account.refresh_token",
        "store.all_products",
        "sync.pull",
    }  # tested elsewhere
    for group in (
        "account",
        "store",
        "products",
        "sync",
        "ai",
        "reading",
        "media",
        "messages",
        "telemetry",
        "web",
        "firebase",
    ):
        for name in dir(getattr(ot, group)):
            if not name.startswith("_"):
                assert f"{group}.{name}" in covered, f"{group}.{name} has no test"


def form(req: httpx.Request) -> dict[str, list[str]]:
    return parse_qs(req.content.decode())


class TestParameters:
    def test_signup_overrides_credentials(self, ot, rec):
        ot.account.signup("new@example.com", "pw2", first_name="Ann", subscribe_to_newsletter=1)
        f = form(rec.last)
        assert f["user"] == ["new@example.com"] and f["pass"] == ["pw2"]
        assert f["first_name"] == ["Ann"] and f["subscribe_to_newsletter"] == ["1"]

    def test_forgot_password_email(self, ot, rec):
        ot.account.forgot_password("a@b.c")
        assert form(rec.last)["email"] == ["a@b.c"]

    def test_web_handoff_storefront(self, ot, rec):
        ot.account.web_handoff_token("US")
        assert form(rec.last)["storefront_code"] == ["US"]

    def test_access_token_stores_tokens(self, ot, rec):
        rec.route(
            "/access_token", httpx.Response(200, json={"authentication_token": "a", "refresh_token": "r"})
        )
        ot.account.access_token()
        assert (ot.token, ot.refresh_token) == ("a", "r")

    def test_search_query(self, ot, rec):
        ot.store.search("study bible", page=2)
        assert rec.last.url.params["q"] == "study bible" and form(rec.last)["page"] == ["2"]

    def test_wishlist_fields(self, ot, rec):
        ot.store.wishlist_add(10, 20)
        assert form(rec.last)["productId"] == ["10"] and form(rec.last)["wishlistId"] == ["20"]
        ot.store.wishlist_remove(10)
        assert "wishlistId" not in form(rec.last)

    def test_category_extra_fields(self, ot, rec):
        ot.store.category(3, sort="title")
        assert form(rec.last)["sort"] == ["title"]

    def test_product_updates_json(self, ot, rec):
        ot.products.updates({"products": [1]})
        assert json.loads(rec.last.content) == {"products": [1]}
        ot.products.updates()
        assert rec.last.content == b"{}"

    def test_email_signup_fields(self, ot, rec):
        ot.products.email_signup("a@b.c", bibles="KJV", token="t")
        assert form(rec.last) == {**form(rec.last), "email": ["a@b.c"], "bibles": ["KJV"], "token": ["t"]}

    def test_reading_templates_ids(self, ot, rec):
        ot.products.reading_templates(4, 5)
        assert rec.last.url.params["templateIds"] == "4,5"

    def test_ai_query_body(self, ot, rec):
        ot.ai.query("grace", books=["Romans"])
        assert rec.last.content == b'{"query":"grace","filters":{"books":["Romans"]}}'
        ot.ai.query("grace")
        assert rec.last.content == b'{"query":"grace"}'

    def test_ai_set_usage_body(self, ot, rec):
        ot.ai.set_usage(5, 1, 10)
        assert json.loads(rec.last.content) == {"input_tokens": 5, "output_tokens": 1, "requests": 10}

    def test_daily_reading_params(self, ot, rec):
        ot.reading.daily_reading("template_versions", template_ids="1,2")
        p = rec.last.url.params
        assert (p["type"], p["template_ids"], p["supportsDevotionalPlans"]) == (
            "template_versions",
            "1,2",
            "true",
        )

    def test_verse_of_the_day_params(self, ot, rec):
        ot.reading.verse_of_the_day("2026-11-08", version="KJV")
        assert dict(rec.last.url.params) == {"date": "2026-11-08", "version": "KJV"}
        ot.reading.verse_of_the_day("2026-11-08")
        assert dict(rec.last.url.params) == {"date": "2026-11-08"}

    def test_media_returns_bytes(self, ot, rec):
        rec.route("/1.jpg", httpx.Response(200, content=b"\xff\xd8", headers={"content-type": "image/jpeg"}))
        assert ot.media.cover(1) == b"\xff\xd8"

    def test_messages_bodies(self, ot, rec):
        ot.messages.list()
        assert json.loads(rec.last.content) == {"install_id": "dev-1"}
        ot.messages.metrics(3, {"seen": 1})
        assert json.loads(rec.last.content) == {
            "install_id": "dev-1",
            "message_id": 3,
            "metrics": {"seen": 1},
        }

    def test_get_variant_params(self, ot, rec):
        ot.telemetry.get_variant("exp", customer_id=9)
        assert dict(rec.last.url.params) == {
            "experiment_id": "exp",
            "install_id": "dev-1",
            "customer_id": "9",
        }

    def test_web_bridge_params(self, ot, rec):
        ot.web.app_to_web_bridge(productid=1, login_handoff_token="h")
        assert dict(rec.last.url.params) == {"productid": "1", "login_handoff_token": "h"}

    def test_product_page_param(self, ot, rec):
        ot.web.product_page(36163)
        assert rec.last.url.params["productid"] == "36163"
