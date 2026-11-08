"""Synchronous HTTP transport."""

from __future__ import annotations

from typing import Any

import httpx

from pyolivetree._transport.base import OperationSpec, build_url, encode_body, parse_response
from pyolivetree.auth import AuthManager


class SyncTransport:
    """Execute synchronous HTTP requests against the Olive Tree API."""

    def __init__(self, auth: AuthManager, *, timeout: float = 30.0) -> None:
        """Initialize sync transport.

        Args:
            auth: Authentication manager for headers and signing.
            timeout: Request timeout in seconds.

        Raises:
            None.
        """
        self._auth = auth
        self._client = httpx.Client(timeout=timeout, follow_redirects=True)

    def close(self) -> None:
        """Close the underlying HTTP client.

        Returns:
            None.

        Raises:
            None.
        """
        self._client.close()

    def __enter__(self) -> SyncTransport:
        """Enter context manager.

        Returns:
            This transport instance.
        """
        return self

    def __exit__(self, *args: object) -> None:
        """Exit context manager and close the client.

        Returns:
            None.
        """
        self.close()

    def request(
        self,
        spec: OperationSpec,
        *,
        path_params: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        data: dict[str, Any] | list[Any] | bytes | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> Any:
        """Perform a synchronous API request.

        Args:
            spec: Operation metadata.
            path_params: Path parameter values.
            query: Query string parameters.
            data: Request body payload.
            extra_headers: Additional headers to merge.

        Returns:
            Parsed response body.

        Raises:
            OliveTreeAPIError: On HTTP error responses.
            OliveTreeAuthError: When HMAC signing is required but no key is set.
        """
        path_params = path_params or {}
        query = query or {}
        url = build_url(spec.server_url, spec.path, path_params)
        body_bytes, content_type = encode_body(spec.content_type, data)
        headers = dict(self._auth.auth_headers(spec.security, server_url=spec.server_url))
        if extra_headers:
            headers.update(extra_headers)
        if self._auth.needs_hmac(spec.security) and body_bytes is not None:
            headers["signature"] = self._auth.sign_body(
                body_bytes, profile=spec.hmac_profile
            )
        if content_type:
            headers["Content-Type"] = content_type
        auth = self._auth.basic_auth(spec.security, server_url=spec.server_url)
        response = self._client.request(
            spec.method.upper(),
            url,
            params=_clean_params(query),
            content=body_bytes,
            headers=headers,
            auth=auth,
        )
        return parse_response(
            spec.operation_id,
            response.status_code,
            response.content,
            response.headers.get("content-type"),
            spec=spec,
        )


def _clean_params(query: dict[str, Any]) -> dict[str, Any]:
    """Remove None values from query parameters.

    Args:
        query: Raw query mapping.

    Returns:
        Query mapping without None values.
    """
    return {key: value for key, value in query.items() if value is not None}
