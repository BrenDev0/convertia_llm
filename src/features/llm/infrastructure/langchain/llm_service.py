from langchain_openai import ChatOpenAI
from ...domain import LlmService

class LangchainLlmService(LlmService):
    def __init__(self):
        self.__model = "gpt-4o"

    
    def _get_agent(
        self,
        temperature: float,
    ):
        return ChatOpenAI(
            model=self.__model,
            temperature=temperature,
            streaming=True
        )

    
    async def interact(
        self,
        temperature: float,
        prompt: str
    ):
        llm = self._get_agent(
            temperature=temperature
        )

        async for chunk in llm.astream(prompt):
            yield chunk.content
        