from abc import ABC, abstractmethod

class LlmService(ABC):
    @abstractmethod
    async def interact(
        self,
        temperature: float,
        prompt: str
    ):
        raise NotImplementedError