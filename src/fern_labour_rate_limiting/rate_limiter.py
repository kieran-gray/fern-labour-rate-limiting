from typing import Protocol, runtime_checkable


@runtime_checkable
class RateLimiter(Protocol):
    """Protocol for rate limiting requests."""

    def is_allowed(self, key: str) -> bool:
        """Checks if the action associated with the key is allowed under the limit."""
