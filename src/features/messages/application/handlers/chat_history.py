import json
from typing import List, Dict, Any
from src.broker import AsyncHandler, ChatsProducer, ChatEvent
from src.persistence import SessionRepository

from ...domain import CreateMessagePayload

class ChatHistoryHandler(AsyncHandler):
    def __init__(
        self,
        session_repository: SessionRepository,
        chats_producer: ChatsProducer
    ):
        self.__session_repository = session_repository
        self.__chats_producer = chats_producer

    async def handle(self, event):
        parsed_event = ChatEvent(**event)
        payload = CreateMessagePayload(**parsed_event.payload)

        key = f"{parsed_event.connection_id}_chat_history"
        session: List[Dict[str, Any]] = self.__session_repository.get_session(key)

        if not session:
            session = [
                payload.model_dump()
            ]

            self.__session_repository.set_session(
                key=key,
                value=json.dumps(session),
                expire_seconds=1800
            )

            if payload.transctipts:
                await self.__chats_producer.publish(
                    routing_key="chats.chat.create",
                    event=parsed_event
                )

            return 
        
        
        chat_history_length = len(session)

        session.insert(0, payload.model_dump())

        if chat_history_length > 6:
            session.pop()

        self.__session_repository.set_session(
            key=key,
            value=json.dumps(session),
            expire_seconds=1800
        )

        if payload.transcripts:
            await self.__chats_producer.publish(
                routing_key="chats.message.create", 
                event=parsed_event
            )
        


        



        