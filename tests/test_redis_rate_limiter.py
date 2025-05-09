import logging
from unittest.mock import Mock

import pytest
from fakeredis import FakeRedis
from redis import Redis, RedisError

from fern_labour_rate_limiting.redis_rate_limiter import RedisRateLimiter

MODULE = "fern_labour_rate_limiting.redis"


@pytest.fixture
def redis() -> Redis:
    return FakeRedis()


def test_rate_limit_allowed(redis: Redis) -> None:
    rate_limiter = RedisRateLimiter(redis=redis, limit=1, expiry=60)
    assert rate_limiter.is_allowed(key="test:key")


def test_rate_limit_exceeded(redis: Redis) -> None:
    rate_limiter = RedisRateLimiter(redis=redis, limit=0, expiry=60)
    assert not rate_limiter.is_allowed(key="test:key")


def test_redis_error_returns_true(caplog: pytest.LogCaptureFixture) -> None:
    redis = Mock()
    redis.incr = Mock(side_effect=RedisError())
    rate_limiter = RedisRateLimiter(redis=redis, limit=1, expiry=60)
    with caplog.at_level(logging.ERROR, MODULE):
        assert rate_limiter.is_allowed(key="test:key")
        assert len(caplog.records) == 1
        assert "Redis error during rate limit check for key" in caplog.messages[0]


def test_exception_returns_true(caplog: pytest.LogCaptureFixture) -> None:
    redis = Mock()
    redis.incr = Mock(side_effect=Exception())
    rate_limiter = RedisRateLimiter(redis=redis, limit=1, expiry=60)
    with caplog.at_level(logging.ERROR, MODULE):
        assert rate_limiter.is_allowed(key="test:key")
        assert len(caplog.records) == 1
        assert "Unexpected error during rate limit check for key" in caplog.messages[0]
