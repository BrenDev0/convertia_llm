import logging
from fastapi import APIRouter, Request, Depends, Body
from fastapi.responses import JSONResponse
from uuid import UUID
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.features.document_processing.domain.schemas import KnowledgeBaseRequest, ExtractTextPayload
from src.broker.dependencies.producers import get_documents_producer
from src.broker.domain import base_event, producer

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(verify_hmac)]
)


@router.post("/Knowledge-base", status_code=202)
def upload(
    doc: KnowledgeBaseRequest = Body(...),
    producer: producer.Producer = Depends(get_documents_producer)
):
    payload = {}

    event = base_event.BaseEvent(
        connection_id=doc.connection_id,
        payload=payload.model_dump()
    )

    producer.publish(
        routing_key="documents.raw",
        event=event
    )

    return JSONResponse(status_code=202, content={"detail": "Request received"})