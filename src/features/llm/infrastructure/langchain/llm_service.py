from langchain_openai import ChatOpenAI
from ...domain import LlmService

class LangchainLlmService(LlmService):
    def __init__(self):
        self.__model = "gpt-4o"

    
    def _get_agent(
        self,
        max_tokens: int,
        temperature: float,
    ):
        return ChatOpenAI(
            model=self.__model,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=True
        )

    
    async def interact(
        self,
        max_tokens: int,
        temperature: float,
        prompt: str
    ):
        llm = self._get_agent(
            max_tokens=max_tokens,
            temperature=temperature
        )

        async for chunk in llm.astream(prompt):
            yield chunk.content
        