import json
from src.persistence.domain.session_repository import SessionRepository
from src.broker.domain import base_event, handlers
from src.features.sessions.domain.schemas import UpdateEmbeddingSessionPayload

class UpdateEmbeddingSession(handlers.Handler):
    def __init__(
        self,
        session_repository: SessionRepository
    ):
        self.__session_repository = session_repository

    def handle(self, event):
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