import logging
from uuid import uuid4
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.broker import PikaAioAsyncProducer, BaseEvent, AsyncProducer
from ...domain import DownloadDocumentPayloadRest, ExtractTextPayload


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

def get_producer():
    return PikaAioAsyncProducer(
        exchange="documents"
    )

@router.post("/", status_code=202)
async def process_document(
    payload: DownloadDocumentPayloadRest = Body(...),
    producer: AsyncProducer = Depends(get_producer)
): 
    extract_text_payload = ExtractTextPayload(
        knowledge_id=payload.knowledge_id,
        file_type=payload.file_type,
        file_url=payload.file_url
    )

    event = BaseEvent(
        event_id=uuid4(),
        user_id=payload.user_id,
        agent_id=payload.agent_id,
        connection_id=payload.connection_id,
        payload=extract_text_payload.model_dump()
    )
 
    await producer.publish(
        routing_key="documents.incomming",
        event=event
    )

    return JSONResponse(status_code=202, content={"detail": "Request received"})