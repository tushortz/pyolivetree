"""Parametrized tests for all generated API operations."""

from __future__ import annotations

import httpx
import pytest
import respx

from pyolivetree import AsyncOliveTreeClient, OliveTreeClient
from pyolivetree._operations import OPERATIONS
from tests.operation_registry import OPERATION_CALLS


def _mock_response(spec_operation_id: str) -> httpx.Response:
    """Build a mock HTTP response for an operation.

    Args:
        spec_operation_id: OpenAPI operationId.

    Returns:
        httpx.Response suitable for respx mocking.
    """
    spec = OPERATIONS[spec_operation_id]
    if spec.response_binary:
        return httpx.Response(200, content=b"binary", headers={"content-type": "image/jpeg"})
    if spec.response_text:
        return httpx.Response(200, text="<html>ok</html>", headers={"content-type": "text/html"})
    return httpx.Response(200, json={"ok": True})


def _mock_routes() -> None:
    """Register respx routes for all operations."""
    for _, _, operation_id, _ in OPERATION_CALLS:
        spec = OPERATIONS[operation_id]
        url = f"{spec.server_url}{spec.path}"
        for param in [
            "{productId}",
            "{productIds}",
            "{categoryId}",
            "{code}",
            "{basePlanId}",
            "{subscriptionId}",
            "{dynamicPath}",
            "{selectionId}",
            "{fromDate}",
            "{toDate}",
            "{locale}",
            "{path}",
            "{month}",
            "{day}",
            "{templateId}",
            "{size}",
        ]:
            if param in url:
                part = param.strip("{}")
                url = url.replace(
                    param, "1" if "Id" in part or part in {"month", "day", "size"} else "test"
                )
        method = spec.method.lower()
        respx.route(method=method, url__regex=url.replace("/", r"\/").replace("1", r"[^/]+"))


@pytest.mark.parametrize("module,method,operation_id,kwargs", OPERATION_CALLS)
@respx.mock
def test_sync_operation(module: str, method: str, operation_id: str, kwargs: dict) -> None:
    """Each sync resource method returns a parsed response."""
    spec = OPERATIONS[operation_id]
    pattern = _url_pattern(spec)
    respx.route(method=spec.method.upper(), url__regex=pattern).mock(
        return_value=_mock_response(operation_id)
    )
    if spec.security and any("OTBearerAuth" in item for item in spec.security):
        respx.post("https://www.olivetree.com/store/br5/app/json/account/account_login").mock(
            return_value=httpx.Response(
                200,
                json={"authenticated": True, "authentication_token": "tok"},
            )
        )
    client = OliveTreeClient(
        username="u",
        password="p",
        install_id="i",
        access_token="tok" if not spec.security else None,
        hmac_key=(
            "ab" * 32
            if spec.security and any("HMACSignature" in s for s in spec.security)
            else None
        ),
    )
    resource = getattr(client, module)
    fn = getattr(resource, method)
    result = fn(**kwargs)
    assert result is not None or result == {}
    client.close()


@pytest.mark.parametrize("module,method,operation_id,kwargs", OPERATION_CALLS)
@respx.mock
@pytest.mark.asyncio
async def test_async_operation(module: str, method: str, operation_id: str, kwargs: dict) -> None:
    """Each async resource method returns a parsed response."""
    spec = OPERATIONS[operation_id]
    pattern = _url_pattern(spec)
    respx.route(method=spec.method.upper(), url__regex=pattern).mock(
        return_value=_mock_response(operation_id)
    )
    if spec.security and any("OTBearerAuth" in item for item in spec.security):
        respx.post("https://www.olivetree.com/store/br5/app/json/account/account_login").mock(
            return_value=httpx.Response(
                200,
                json={"authenticated": True, "authentication_token": "tok"},
            )
        )
    client = AsyncOliveTreeClient(
        username="u",
        password="p",
        install_id="i",
        access_token="tok" if not spec.security else None,
        hmac_key=(
            "ab" * 32
            if spec.security and any("HMACSignature" in s for s in spec.security)
            else None
        ),
    )
    resource = getattr(client, module)
    fn = getattr(resource, f"a{method}")
    result = await fn(**kwargs)
    assert result is not None or result == {}
    await client.aclose()


def _url_pattern(spec: object) -> str:
    """Convert an operation path to a regex pattern for respx.

    Args:
        spec: OperationSpec instance.

    Returns:
        Regex pattern matching the operation URL.
    """
    from pyolivetree._transport.base import OperationSpec

    assert isinstance(spec, OperationSpec)
    path = spec.path
    import re

    escaped = re.escape(f"{spec.server_url}{path}")
    escaped = re.sub(r"\\\{[^}]+\\\}", r"[^/]+", escaped)
    return escaped
