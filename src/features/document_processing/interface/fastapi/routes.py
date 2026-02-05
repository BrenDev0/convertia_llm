import logging
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.di.container import Container
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.features.document_processing.domain.schemas import DownloadDocumentPayload, ExtractTextPayload
from src.broker.domain import base_event, producer

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
    doc_producer: producer.Producer = Container.resolve("documents_producer")

    embedings_session_payload = {
        "knowledge_id": str(payload.knowledge_id),
        "session": {
            "stage": "Descargando documento...",
            "status": "Descargando",
            "progress": 50
        }
    }

    event = base_event.BaseEvent(
        user_id=payload.user_id,
        agent_id=payload.agent_id,
        connection_id=payload.connection_id,
        payload=embedings_session_payload
    )

    doc_producer.publish(
        routing_key="documents.sessions.embeddings_update",
        event=event
    )
    
    extract_text_payload = ExtractTextPayload(
        knowledge_id=payload.knowledge_id,
        file_type=payload.file_type,
        file_url=payload.file_url
    )

    event.payload = extract_text_payload.model_dump()

    doc_producer.publish(
        routing_key="documents.incomming",
        event=event
    )

    return JSONResponse(status_code=202, content={"detail": "Request received"})