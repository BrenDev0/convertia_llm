import logging
from uuid import uuid4
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.di.container import Container
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.features.document_processing.domain.schemas import DownloadDocumentPayload, ExtractTextPayload
from src.broker.domain import base_event, producer
from src.broker.infrastructure.pika.producer import RabbitMqProducer

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(verify_hmac)]
)

def get_producer():
    return RabbitMqProducer(
        exchange="documents"
    )

@router.post("/knowledge-base", status_code=202)
def upload(
    payload: DownloadDocumentPayload = Body(...),
    producer: producer.Producer = Depends(get_producer)
): 
    extract_text_payload = ExtractTextPayload(
        knowledge_id=payload.knowledge_id,
        file_type=payload.file_type,
        file_url=payload.file_url
    )

    event = base_event.BaseEvent(
        event_id=uuid4(),
        user_id=payload.user_id,
        agent_id=payload.agent_id,
        connection_id=payload.connection_id,
        payload=extract_text_payload.model_dump()
    )

    update_status_payload = {
        "knowledge_id": payload.knowledge_id,
        "status": "PROCESSING"
    }

    event.payload = update_status_payload
    
    producer.publish(
        routing_key="documents.status.update",
        event=event
    )
    
    producer.publish(
        routing_key="documents.incomming",
        event=event
    )

    return JSONResponse(status_code=202, content={"detail": "Request received"})