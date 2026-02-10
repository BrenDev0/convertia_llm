from abc import ABC, abstractmethod
from typing import Dict, Any

class Consumer(ABC):
    @abstractmethod
    def start(self):
      raise NotImplementedError

    @abstractmethod
    def handle(self, payload: Dict[str, Any]):
        raise NotImplementedError
    
  
class AsyncConsumer(ABC):
    @abstractmethod
    def start(self):
      raise NotImplementedError

    @abstractmethod
    async def handle(self, payload: Dict[str, Any]):
        raise NotImplementedError

    