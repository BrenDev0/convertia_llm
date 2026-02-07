from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class SessionRepository(ABC):
    @abstractmethod
    def set_session(self, key: str, value: str, expire_seconds: Optional[int] = 3600) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_session(self, key: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
    
    @abstractmethod
    def delete_session(self, key: str) -> bool:
        raise NotImplementedError
    
  