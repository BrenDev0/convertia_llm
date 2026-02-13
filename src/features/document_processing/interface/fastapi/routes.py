import logging
from uuid import uuid4
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.features.document_processing.domain.schemas import DownloadDocumentPayloadRest, ExtractTextPayload
from src.broker.domain import base_event, producer
from src.broker.infrastructure.pikaaio.async_producer import RabbitMqAsyncProducer

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(verify_hmac)]
)

def get_producer():
    return RabbitMqAsyncProducer(
        exchange="documents"
    )

@router.post("/", status_code=202)
def process_document(
    payload: DownloadDocumentPayloadRest = Body(...),
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
 
    producer.publish(
        routing_key="documents.incomming",
        event=event
    )

    return JSONResponse(status_code=202, content={"detail": "Request received"})