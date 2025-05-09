from fern_labour_rate_limiting.rate_limiter import RateLimiter


class MockRateLimiter:
    def is_allowed(self, key: str) -> bool:
        return True


def test_implementation_is_subclass() -> None:
    assert issubclass(MockRateLimiter, RateLimiter)
