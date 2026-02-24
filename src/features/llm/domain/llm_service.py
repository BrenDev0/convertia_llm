from abc import ABC, abstractmethod

class LlmService(ABC):
    @abstractmethod
    async def interact(
        self,
        max_tokens: int,
        temperature: float,
        prompt: str
    ):
        raise NotImplementedError