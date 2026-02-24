from abc import ABC, abstractmethod

class LlmService(ABC):
    @abstractmethod
    async def interact(self, prompt: str):
        raise NotImplementedError