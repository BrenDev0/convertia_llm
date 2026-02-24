from src.persistence import SessionRepository
from uuid import UUID
from typing import List, Dict, Any

class GetRAGChatHistory:
    def __init__(
        self,
        session_repository: SessionRepository
    ):
        self.__session_repository = session_repository

    def execute(
        self,
        chat_id: UUID,
        prompt: str
    ):
        

        key = f"{chat_id}_chat_history"
        chat_history: List[Dict[str, Any]] = self.__session_repository.get_session(key)

        if chat_history:
            messages = [
                "\n\nCONVERSATION HISTORY:"
            ]
            
            for msg in chat_history:
                messages.append(
                    f"{msg["type"]}: {msg["text"]}"
                )
            
            prompt = prompt + " ".join(messages)
        
        return prompt
        
