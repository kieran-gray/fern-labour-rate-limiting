from redis import Redis

from fern_labour_rate_limiting.redis_rate_limiter import RedisRateLimiter


def can_instantiate_classes() -> None:
    RedisRateLimiter(redis=Redis(), limit=1, expiry=10)
    print("Can instantiate all classes")


if __name__ == "__main__":
    can_instantiate_classes()
