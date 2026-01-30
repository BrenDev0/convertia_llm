from abc import ABC, abstractmethod
from typing import Union, Dict, Any
from pydantic import BaseModel

class Producer(ABC):
    @abstractmethod
    def publish(
        self,
        routing_key: str,
        event: Union[BaseModel, Dict[str, Any]]  
    ):
        raise NotImplementedError