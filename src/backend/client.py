import redis.asyncio as redis

redis_client: redis.Redis | None=None


def get_redis_client() -> redis.Redis:

    if redis_client is None:

        raise RuntimeError('Redis client is not initializied')

    return redis_client