from abc import ABC, abstractmethod
from typing import Dict, Any

class Handler(ABC):
    @abstractmethod
    def handle(self, event: Dict[str, Any]):
        raise NotImplementedError
    
class AsyncHandler(ABC):
    @abstractmethod
    async def handle(self, event: Dict[str, Any]):
        raise NotImplementedError