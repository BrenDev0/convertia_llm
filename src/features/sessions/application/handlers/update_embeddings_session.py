import json
from src.persistence.domain.session_repository import SessionRepository
from src.broker.domain import base_event, handlers, producer
from src.features.sessions.domain.schemas import UpdateEmbeddingSessionPayload

class UpdateEmbeddingSession(handlers.Handler):
    def __init__(
        self,
        session_repository: SessionRepository,
        producer: producer.AsyncProducer
    ):
        self.__session_repository = session_repository
        self.__producer = producer

    async def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
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

