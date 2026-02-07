import json
from typing import Optional, Dict, Any
from redis import Redis
import os
from src.persistence.domain.session_repository import SessionRepository


class RedisSessionRepository(SessionRepository):
    def __init__(self):
        self.__connection_url = os.getenv("REDIS_URL")

        if not self.__connection_url:
            raise ValueError("Redis variable not configured")
        
        self.redis = Redis.from_url(url=self.__connection_url)

    def set_session(self, key: str, value: str, expire_seconds: Optional[int] = 3600) -> None:       
        self.redis.set(key, value, ex=expire_seconds)

    def get_session(self, key: str) -> Optional[Dict[str, Any]]:
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def delete_session(self, key: str) -> bool:
        return self.redis.delete(key) > 0