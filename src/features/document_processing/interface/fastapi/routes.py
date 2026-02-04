import logging
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.di.container import Container
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.features.document_processing.domain.schemas import DownloadDocumentPayload
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

    event = base_event.BaseEvent(
        connection_id=payload.connection_id,
        payload=payload.model_dump()
    )

    doc_producer: producer.Producer = Container.resolve("documents_producer")

    doc_producer.publish(
        routing_key="documents.incomming",
        event=event
    )

    return JSONResponse(status_code=202, content={"detail": "Request received"})