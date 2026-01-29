from abc import ABC, abstractmethod
from typing import Dict, Any

class Handler(ABC):
    @abstractmethod
    def handle(self, payload: Dict[str, Any]):
        raise NotImplementedError
    
class AsyncHandler(ABC):
    @abstractmethod
    async def handle(self, payload: Dict[str, Any]):
        raise NotImplementedError