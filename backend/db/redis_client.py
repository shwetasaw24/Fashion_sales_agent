# backend/db/redis_client.py
import redis
import logging
import os

logger = logging.getLogger(__name__)

# Check if we should use fake redis for development
USE_FAKE_REDIS = os.getenv("USE_FAKE_REDIS", "false").lower() == "true"

if USE_FAKE_REDIS:
    try:
        import fakeredis
        redis_client = fakeredis.FakeStrictRedis(decode_responses=True)
        logger.info("✅ Using FakeRedis for development (in-memory)")
    except ImportError:
        logger.error("FakeRedis not installed. Install with: pip install fakeredis")
        raise
else:
    try:
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
            socket_connect_timeout=5,  # 5 second timeout for connection
            socket_timeout=5  # 5 second timeout for operations
        )
        # Test connection
        redis_client.ping()
        logger.info("✅ Redis connected successfully")
    except redis.ConnectionError as e:
        logger.error(f"❌ Cannot connect to Redis at {os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}")
        logger.error("Options to fix:")
        logger.error("  1. Start Redis: docker run -d -p 6379:6379 redis:7")
        logger.error("  2. Or install locally: winget install Redis.Redis")
        logger.error("  3. Or use FakeRedis for dev: export USE_FAKE_REDIS=true")
        raise
