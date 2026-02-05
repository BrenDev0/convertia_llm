import logging
import json
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.di.container import Container
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.features.document_processing.domain.schemas import DownloadDocumentPayload, ExtractTextPayload
from src.broker.domain import base_event, producer
from src.persistence.domain.session_repository import SessionRepository

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(verify_hmac)]
)


@router.post("/Knowledge-base", status_code=202)
def upload(
    payload: DownloadDocumentPayload = Body(...)
):
    session_repository: SessionRepository = Container.resolve("session_repository")
    key = f"{payload.agent_id}_embeddings_tracker"

    session = session_repository.get_session(
        key=key
    )

    if session:
        session[payload.knowledge_id] = {
            "stage": "Descargando documento...",
            "status": "Descargando",
            "status": 50
        }

    else: 
        session = {
            str(payload.knowledge_id): {
                "stage": "Descargando documento...",
                "status": "Descargando",
                "status": 50
            }
        }

    session_repository.set_session(
        key=key,
        value=json.dumps(session)
    )
    
    extract_text_payload = ExtractTextPayload(
        knowledge_id=payload.knowledge_id,
        file_type=payload.file_type,
        file_url=payload.file_url
    )

    event = base_event.BaseEvent(
        user_id=payload.user_id,
        agent_id=payload.agent_id,
        connection_id=payload.connection_id,
        payload=extract_text_payload.model_dump()
    )

    doc_producer: producer.Producer = Container.resolve("documents_producer")

    doc_producer.publish(
        routing_key="documents.incomming",
        event=event
    )

    return JSONResponse(status_code=202, content={"detail": "Request received"})