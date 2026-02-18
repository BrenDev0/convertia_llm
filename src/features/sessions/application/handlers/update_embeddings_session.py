import json
from src.persistence import SessionRepository
from src.broker import AsyncHandler, CommunicationProducer, BaseEvent
from ...domain import UpdateEmbeddingSessionPayload

class UpdateEmbeddingSession(AsyncHandler):
    def __init__(
        self,
        session_repository: SessionRepository,
        producer: CommunicationProducer
    ):
        self.__session_repository = session_repository
        self.__producer = producer

    async def handle(self, event):
        parsed_event = BaseEvent(**event)
        payload = UpdateEmbeddingSessionPayload(**parsed_event.payload)

        key = f"{parsed_event.agent_id}_embeddings_tracker"
        session = self.__session_repository.get_session(key=key)
   
        if session:
            session[str(payload.knowledge_id)] = payload.update

        else: 
            session = {
                str(payload.knowledge_id): payload.update
            }

        self.__session_repository.set_session(
            key=key,
            value=json.dumps(session)
        )

        broadcast_payload = {
            "type":"STATUS",
            "data": {
                **payload.update,
                "knowledge_id": str(payload.knowledge_id)
            }
        }

        event_copy = parsed_event.model_copy()
        event_copy.payload = broadcast_payload

        await self.__producer.publish(
            routing_key="communication.websocket.broadcast",
            event=event_copy
        )

