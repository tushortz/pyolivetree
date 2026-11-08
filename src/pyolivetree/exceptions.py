"""Client exceptions."""


class OliveTreeError(Exception):
    """Base exception for pyolivetree errors."""


class OliveTreeAPIError(OliveTreeError):
    """Raised when the API returns a non-success HTTP status."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        operation_id: str,
        body: str | bytes | dict | list | None = None,
    ) -> None:
        """Initialize an API error.

        Args:
            message: Human-readable error description.
            status_code: HTTP status code from the response.
            operation_id: OpenAPI operationId for the failed request.
            body: Raw or parsed response body, if available.

        Raises:
            None.
        """
        super().__init__(message)
        self.status_code = status_code
        self.operation_id = operation_id
        self.body = body


class OliveTreeAuthError(OliveTreeError):
    """Raised when authentication or token refresh fails."""

    def __init__(self, message: str) -> None:
        """Initialize an auth error.

        Args:
            message: Human-readable error description.

        Raises:
            None.
        """
        super().__init__(message)
