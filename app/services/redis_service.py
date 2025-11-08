import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def add_to_blacklist(jti: str):
    """Додає JTI (ідентифікатор токена) у чорний список на 1 годину."""
    await redis_client.setex(f"blacklist:{jti}", 3600, "true")

async def is_blacklisted(jti: str) -> bool:
    """Перевіряє, чи є JTI у чорному списку."""
    return await redis_client.exists(f"blacklist:{jti}") == 1
