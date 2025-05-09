import logging

from redis import Redis, RedisError

from fern_labour_rate_limiting.rate_limiter import RateLimiter

log = logging.getLogger(__name__)


class RedisRateLimiter(RateLimiter):
    def __init__(self, redis: Redis, limit: int, expiry: int) -> None:
        self._redis = redis
        self._limit = limit
        self._expiry = expiry

    def is_allowed(self, key: str) -> bool:
        log.debug(f"Running rate-limit check for {key=}")
        try:
            current_count = self._redis.incr(key)
            if current_count == 1:
                self._redis.expire(name=key, time=self._expiry)
                log.debug(f"Key '{key}' created.")
            log.debug(f"Current count for {key} = {current_count}")
            if current_count > self._limit:  # type: ignore
                log.warning(f"Rate limit exceeded for key '{key}'")
                return False
            return True
        except RedisError as e:
            log.error(f"Redis error during rate limit check for key '{key}': {e}")
            return True
        except Exception as e:
            log.error(f"Unexpected error during rate limit check for key '{key}': {e}")
            return True
