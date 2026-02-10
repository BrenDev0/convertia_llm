import logging
import os
import hmac
import hashlib
import time
from uuid import UUID, uuid4
from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect, Depends
from src.broker.domain import producer, base_event
from src.broker.infrastructure.pika.producer import RabbitMqProducer
from src.features.websocket.container import WebsocketConnectionsContainer
from src.features.websocket.domain import schemas, exceptions
from src.features.knowledge_base.domain.schemas import DeleteEmbeddingsPayload
from src.features.document_processing.domain.schemas import DownloadDocumentPayloadWebsocket


logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Websocket"]
)

def verify_hmac_ws(signature: str, payload: str) -> bool:
    """
    Verify HMAC signature for WebSocket connections.
    """
    secret = os.getenv("HMAC_SECRET")
    if not secret:
        logger.error("HMAC variables not set")
        return False
    
    if not signature or not payload:
        logger.debug(f"Missing signature or payload, ::: signature: {signature} ::: payload: {payload}")
        return False
    
    try:
        timestamp = int(payload)

    except ValueError:
        logger.debug(f"Invalid timestamp ::: timestamp: {timestamp}")
        return False
    
    current_time = int(time.time() * 1000)
    allowed_drift = 60_000

    if abs(current_time - timestamp) > allowed_drift:
        logger.debug(f"Expired ::: timestamp: {timestamp}, ::: current_time: {current_time}")
        return False
    
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        logger.debug(f"Comparison failed ::: expected: {expected} ::: received: {signature}")
        return False
    
    return True

ALLOWED_MESSAGE_TYPES = ["EMBED DOCUMENT", "DELETE EMBEDDINGS"]

def get_documents_producer():
    return RabbitMqProducer(
        exchange="documents"
    )

@router.websocket("/llm/{connection_id}")
async def async_ws_connect(
    websocket: WebSocket,
    connection_id: UUID,
    documents_producer: producer.Producer=Depends(get_documents_producer)
):
    params = websocket.query_params

    signature = params.get("x-signature")
    payload = params.get("x-payload")

    if not verify_hmac_ws(signature=signature, payload=payload):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return 

    await websocket.accept()

    WebsocketConnectionsContainer.register_connection(
        connection_id=connection_id,
        websocket=websocket
    )
    logger.debug(f"Websocket connection: {connection_id} closed")

    try:
        while True:
            message = await websocket.receive_json()

            try:
                parsed_message = schemas.WebsocketMessage(**message)

                match parsed_message.type.upper():
                    case "EMBED MESSAGE":
                        try:
                            payload = DownloadDocumentPayloadWebsocket.model_validate(parsed_message.data, by_alias=False)

                        except Exception:
                            logger.debug(f"payload received ::: {parsed_message.data}")
                            raise exceptions.WebsocketException(
                                detail="Invalid data sent for delete embeddings, Expected 'user_id' and 'knowledge_id'"
                            )
                        
                        extract_text_payload = {
                            "knowledge_id": payload.knowledge_id,
                            "file_type": payload.file_type,
                            "file_url": payload.file_url
                        }

                        event = base_event.BaseEvent(
                            event_id=uuid4(),
                            user_id=payload.user_id,
                            agent_id=payload.agent_id,
                            connection_id=connection_id,
                            payload=extract_text_payload
                        )

                        documents_producer.publish(
                            routing_key="documents.incomming",
                            event=event
                        )

                    case "DELETE EMBEDDINGS":
                        try:
                            payload = DeleteEmbeddingsPayload.model_validate(parsed_message.data, by_alias=False)

                        except Exception:
                            logger.debug(f"payload received::: {parsed_message.data}")
                            raise exceptions.WebsocketException(
                                detail="Invalid data sent for delete embeddings, Expected 'user_id' and 'knowledge_id'"
                            )

                        event = base_event.BaseEvent(
                            event_id=uuid4(),
                            connection_id=connection_id,
                            user_id=payload.user_id,
                            payload=payload
                        )

                        documents_producer.publish(
                            routing_key="documents.embeddings.delete",
                            event=event
                        )
                    case _: 
                        raise exceptions.WebsocketException(
                            detail=f"Invalid message type: {parsed_message.type}, Allowed types {', '.join(ALLOWED_MESSAGE_TYPES)}"
                        )
            
            except exceptions.WebsocketException as e:
                error_message = schemas.WebsocketMessage(
                    type="BAD REQUEST",
                    data={
                        "detail": str(e)
                    }
                )

                await websocket.send_json(error_message)
            except Exception:
                error_message = schemas.WebsocketMessage(
                    type="BAD REQUEST",
                    data={
                        "detail": "Invalid message schema" 
                    }
                )
                await websocket.send_json(error_message)

            logger.debug(f"INCOMMING MESSAGE ::: {message}")

    
    except WebSocketDisconnect:
        logger.debug(f'Websocket connection: {connection_id} closed')
        WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)

