"""Shared HTTP transport utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlencode

from pyolivetree.exceptions import OliveTreeAPIError


@dataclass
class OperationSpec:
    """Metadata for a single API operation."""

    operation_id: str
    method: str
    path: str
    summary: str
    tag: str
    security: list[dict[str, list[str]]] = field(default_factory=list)
    hmac_profile: str = "telemetry"
    server_url: str = "https://www.olivetree.com"
    content_type: str | None = None
    response_json: bool = True
    response_text: bool = False
    response_binary: bool = False


def build_url(base: str, path: str, path_params: dict[str, Any]) -> str:
    """Substitute path parameters and join with the server base URL.

    Args:
        base: Server base URL without trailing slash.
        path: OpenAPI path template with {param} placeholders.
        path_params: Values for path parameters.

    Returns:
        Fully qualified request URL.

    Raises:
        KeyError: If a required path parameter is missing.
    """
    resolved = path
    for key, value in path_params.items():
        resolved = resolved.replace("{" + key + "}", str(value))
    return f"{base.rstrip('/')}{resolved}"


def encode_body(
    content_type: str | None, data: dict[str, Any] | list[Any] | bytes | None
) -> tuple[bytes | None, str | None]:
    """Encode a request body for the given content type.

    Args:
        content_type: MIME type for the request body.
        data: Payload to encode.

    Returns:
        Tuple of encoded body bytes and effective content type.

    Raises:
        TypeError: If data type is incompatible with the content type.
    """
    if data is None:
        return None, content_type
    if isinstance(data, bytes):
        return data, content_type
    if content_type == "application/x-www-form-urlencoded":
        if not isinstance(data, dict):
            raise TypeError("form body must be a dict")
        return urlencode(data, doseq=True).encode(), content_type
    if content_type == "application/json":
        return json.dumps(data, separators=(",", ":")).encode(), content_type
    if content_type in (None, ""):
        if isinstance(data, dict):
            return urlencode(data, doseq=True).encode(), "application/x-www-form-urlencoded"
        return json.dumps(data, separators=(",", ":")).encode(), "application/json"
    raise TypeError(f"unsupported content type: {content_type}")


def parse_response(
    operation_id: str,
    status_code: int,
    content: bytes,
    content_type: str | None,
    *,
    spec: OperationSpec,
) -> Any:
    """Parse an HTTP response body based on content type and operation metadata.

    Args:
        operation_id: OpenAPI operationId.
        status_code: HTTP status code.
        content: Raw response bytes.
        content_type: Response Content-Type header value.
        spec: Operation metadata for expected response shape.

    Returns:
        Parsed response as dict, list, str, or bytes.

    Raises:
        OliveTreeAPIError: If the status code indicates failure.
    """
    if status_code >= 400:
        parsed: str | bytes | dict | list | None
        try:
            parsed = json.loads(content.decode()) if content else None
        except (json.JSONDecodeError, UnicodeDecodeError):
            parsed = content
        raise OliveTreeAPIError(
            f"API error {status_code} for {operation_id}",
            status_code=status_code,
            operation_id=operation_id,
            body=parsed,
        )
    if status_code == 302:
        return content.decode("utf-8", errors="replace")
    if spec.response_binary or _is_binary(content_type):
        return content
    if spec.response_text or _is_text(content_type):
        return content.decode("utf-8", errors="replace")
    if not content:
        return {}
    try:
        return json.loads(content.decode())
    except json.JSONDecodeError:
        return content.decode("utf-8", errors="replace")


def _is_binary(content_type: str | None) -> bool:
    """Return True if the content type represents binary data.

    Args:
        content_type: MIME type string.

    Returns:
        True for binary MIME types.
    """
    if not content_type:
        return False
    lowered = content_type.lower()
    return any(
        token in lowered
        for token in ("octet-stream", "image/", "audio/", "video/", "application/zip")
    )


def _is_text(content_type: str | None) -> bool:
    """Return True if the content type represents text or markup.

    Args:
        content_type: MIME type string.

    Returns:
        True for text or XML/HTML MIME types.
    """
    if not content_type:
        return False
    lowered = content_type.lower()
    return any(token in lowered for token in ("text/", "xml", "html"))
