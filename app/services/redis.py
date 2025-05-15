from enum import StrEnum
import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

class RedisService:
    """Service for handling Redis operations"""

    class Namespace:
        """Namespaces for Redis keys"""
        USER = "user"
        """Namespace for user-related keys."""
        RESUME = "resume"
        """Namespace for resume-related keys."""

    class Status(StrEnum):
        """Status values for Redis keys"""
        ACTIVE = "active"
        """Active status."""
        INACTIVE = "inactive"
        """Inactive status."""

    def __init__(self):
        """Initialize Redis connection"""
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

    @classmethod
    def _get_key(cls, namespace: str, key: str) -> str:
        """Get a namespaced key for Redis."""
        return f"{namespace}:{key}"

    def set_user(self, key: str, value: str) -> None:
        """Set a user-related value in Redis."""
        self.redis.set(
            RedisService._get_key(
                RedisService.Namespace.USER, key
            ),
            value
        )

    def get_user(self, key: str) -> str:
        """Get a user-related value from Redis."""
        return self.redis.get(
            RedisService._get_key(
                RedisService.Namespace.USER, key
            )
        )

    def set_resume(self, key: str, value: str) -> None:
        """Set a resume-related value in Redis."""
        self.redis.set(
            RedisService._get_key(
                RedisService.Namespace.RESUME, key
            ),
            value
        )

    def get_resume(self, key: str) -> str:
        """Get a resume-related value from Redis."""
        return self.redis.get(
            RedisService._get_key(
                RedisService.Namespace.RESUME, key
            )
        )

    def set_status(self, key: str, value: Status) -> None:
        """Set a status value in Redis."""
        self.redis.set(
            RedisService._get_key(
                RedisService.Namespace.USER, key
            ),
            value
        )

    def get_status(self, key: str) -> Status:
        """Get a status value from Redis."""
        raw = self.redis.get(
            RedisService._get_key(
                RedisService.Namespace.USER, key
            )
        )
        return raw if raw else RedisService.Status.INACTIVE
