
from enum import StrEnum
from typing import Union, Dict, Any
import json
from redis import Redis
from redis.commands.json.path import Path
from redis.typing import ResponseT
from app import REDIS_URL

class RedisService:
    """Service to interact with Redis."""
    __client = Union[Redis, None]
    """Redis client instance."""

    class Namespace(StrEnum):
        """Namespace for Redis keys."""
        TIME = "time"
        """Namespace for time-related keys."""
        STATUS = "status"
        """Namespace for status-related keys."""
        USER = "user"
        """Namespace for user-related keys."""
        JOB_DESCRIPTION = "job_description"
        """Namespace for job description-related keys."""
        RESUME = "resume"
        """Namespace for resume-related keys."""
        RESUME_RAW_TEXT = "resume_raw_text"
        """Namespace for raw resume text."""
        ENHANCED_RESUME = "enhanced_resume"
        """Namespace for enhanced resume data."""
        FEEDBACK = "feedback"
        """Namespace for feedback-related keys."""

    class Status(StrEnum):
        """Status values for Redis keys."""
        ACTIVE = "active"
        """Active status."""
        INACTIVE = "inactive"
        """Inactive status."""

    def __init__(self):
        """Initialize the RedisService."""
        # Ensure client is connected
        self.get_client()

    @staticmethod
    def connect():
        """Connect to Redis."""
        RedisService.__client = Redis.from_url(REDIS_URL)

    @staticmethod
    def disconnect():
        """Disconnect from Redis."""
        if RedisService.__client is not None:
            RedisService.__client.close()
            RedisService.__client = None

    @staticmethod
    def get_client() -> Redis:
        """Get Redis client."""
        if RedisService.__client is None:
            RedisService.connect()
        return RedisService.__client

    @staticmethod
    def get(key) -> ResponseT:
        """Get a value from Redis."""
        return RedisService.get_client().get(key)

    @staticmethod
    def set(key, value) -> None:
        """Set a value in Redis."""
        RedisService.get_client().set(key, value)

    @staticmethod
    def setKeyWithNamespace(namespace, key, value) -> None:
        """Set a value in Redis with a namespace."""
        RedisService.get_client().set(f"{namespace}:{key}", value)

    @staticmethod
    def getKeyWithNamespace(namespace, key) -> ResponseT:
        """Get a value from Redis with a namespace."""
        return RedisService.get_client().get(f"{namespace}:{key}")

    @staticmethod
    def set_time(key, value) -> None:
        """Set a time-related value in Redis."""
        RedisService.setKeyWithNamespace(RedisService.Namespace.TIME, key, value)

    @staticmethod
    def get_time(key) -> ResponseT:
        """Get a time-related value from Redis."""
        return RedisService.getKeyWithNamespace(RedisService.Namespace.TIME, key)

    @staticmethod
    def set_status(key, value) -> None:
        """Set a status-related value in Redis."""
        RedisService.setKeyWithNamespace(RedisService.Namespace.STATUS, key, value)

    @staticmethod
    def get_status(key) -> Union[str, None]:
        """Get a status-related value from Redis."""
        raw = RedisService.getKeyWithNamespace(RedisService.Namespace.STATUS, key)
        return raw.decode("utf-8") if raw else None

    @staticmethod
    def set_user(key, value) -> None:
        """Set a user-related value in Redis."""
        RedisService.setKeyWithNamespace(RedisService.Namespace.USER, key, value)

    @staticmethod
    def get_user(key) -> ResponseT:
        """Get a user-related value from Redis."""
        raw = RedisService.getKeyWithNamespace(RedisService.Namespace.USER, key)
        return raw.decode("utf-8") if raw else None

    @staticmethod
    def set_job_description(key, value) -> None:
        """Set a job description-related value in Redis."""
        RedisService.setKeyWithNamespace(
            RedisService.Namespace.JOB_DESCRIPTION, key, value
        )

    @staticmethod
    def get_job_description(key) -> ResponseT:
        """Get a job description-related value from Redis."""
        raw = RedisService.getKeyWithNamespace(
            RedisService.Namespace.JOB_DESCRIPTION, key
        )
        return raw.decode("utf-8") if raw else None

    @staticmethod
    def set_resume(key, value) -> None:
        """Set a resume-related value in Redis."""
        RedisService.setKeyWithNamespace(RedisService.Namespace.RESUME, key, value)

    @staticmethod
    def get_resume(key) -> ResponseT:
        """Get a resume-related value from Redis."""
        raw = RedisService.getKeyWithNamespace(RedisService.Namespace.RESUME, key)
        return raw.decode("utf-8") if raw else None

    @staticmethod
    def set_feedback(key, value: dict) -> None:
        """Set a feedback-related value in Redis."""
        RedisService.get_client().json().set(
            f"{RedisService.Namespace.FEEDBACK}:{key}", Path.root_path(), value
        )

    @staticmethod
    def get_feedback(key) -> dict:
        """Get a feedback-related value from Redis."""
        return (
            RedisService.get_client()
            .json()
            .get(f"{RedisService.Namespace.FEEDBACK}:{key}")
        )
    
    """Writing for clarity and """

    async def store_resume_raw_text(self, user_id: str, text: str) -> None:
        """
        Store raw resume text in Redis
        
        Args:
            user_id: The user ID to associate with the resume text
            text: The raw text content of the resume
        """
        RedisService.setKeyWithNamespace(
            RedisService.Namespace.RESUME_RAW_TEXT, user_id, text
        )
    
    async def get_resume_raw_text(self, user_id: str) -> Union[str, None]:
        """
        Get raw resume text from Redis
        
        Args:
            user_id: The user ID to get the resume text for
            
        Returns:
            The raw text of the resume or None if not found
        """
        raw = RedisService.getKeyWithNamespace(
            RedisService.Namespace.RESUME_RAW_TEXT, user_id
        )
        return raw.decode("utf-8") if raw else None
    
    async def store_enhanced_resume(self, user_id: str, job_title: str, data: Dict[str, Any]) -> None:
        """
        Store enhanced resume data in Redis
        
        Args:
            user_id: The user ID to associate with the enhanced resume
            job_title: The job title the resume was enhanced for
            data: The enhanced resume data
        """
        key = f"{user_id}:{job_title}"
        json_data = json.dumps(data)
        RedisService.setKeyWithNamespace(
            RedisService.Namespace.ENHANCED_RESUME, key, json_data
        )
    
    async def get_enhanced_resume(self, user_id: str, job_title: str) -> Union[Dict[str, Any], None]:
        """
        Get enhanced resume data from Redis
        
        Args:
            user_id: The user ID to get the enhanced resume for
            job_title: The job title the resume was enhanced for
            
        Returns:
            The enhanced resume data or None if not found
        """
        key = f"{user_id}:{job_title}"
        raw = RedisService.getKeyWithNamespace(
            RedisService.Namespace.ENHANCED_RESUME, key
        )
        
        if raw:
            return json.loads(raw.decode("utf-8"))
        return None