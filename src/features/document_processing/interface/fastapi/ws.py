import logging
from uuid import UUID, uuid4
from pydantic import ValidationError
from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect, Depends
from src.broker.domain import producer, base_event
from src.broker.infrastructure.pika.producer import RabbitMqProducer
from src.features.websocket.container import WebsocketConnectionsContainer
from src.features.websocket.domain import schemas, exceptions
from src.features.document_processing.domain.schemas import (
    DownloadDocumentPayloadWebsocket,
    ExtractTextPayload
)
from src.security.hmac import verify_hmac_ws


logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Websocket"]
)


ALLOWED_MESSAGE_TYPES = ["process"]

def get_documents_producer():
    return RabbitMqProducer(
        exchange="documents"
    )

@router.websocket("/documents/{connection_id}")
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
            
            except ValidationError:
                logger.error(f"Invalid message schema, received :::{message}")
                raise exceptions.WebsocketException(f"Invalid message schema expected: {', '.join(schemas.WebsocketMessage.model_fields.keys())}")
            
            requested_action = parsed_message.type.split(".")

            if requested_action[0].lower() != "documents" or len(requested_action) < 2:
                raise exceptions.WebsocketException(
                    detail=f"Invalid format for message type, type must have the scope and action separated by a '.'. ex: 'documents.process'. received: {parsed_message.type}"
                )

            match parsed_message.type[1].lower():
                case "process":
                    try:
                        incomming_payload = DownloadDocumentPayloadWebsocket.model_validate(parsed_message.data, by_alias=True)

                    except Exception:
                        raise exceptions.WebsocketException(
                            detail=f"Invalid data sent for delete embeddings, Expected: {', '.join(DownloadDocumentPayloadWebsocket.model_fields.keys())}"
                        )
                    
                    extract_text_payload = ExtractTextPayload(
                        knowledge_id=incomming_payload.knowledge_id,
                        file_type=incomming_payload.file_type,
                        file_url=incomming_payload.file_url
                    )

                    event = base_event.BaseEvent(
                        event_id=uuid4(),
                        connection_id=connection_id,
                        user_id=incomming_payload.user_id,
                        agent_id=incomming_payload.agent_id,
                        payload=extract_text_payload.model_dump()
                    )

                    documents_producer.publish(
                        routing_key="documents.incomming",
                        event=event
                    )
                case _: 
                    raise exceptions.WebsocketException(
                        detail=f"Invalid message type: {parsed_message.type}, Allowed types documents.{', '.join(ALLOWED_MESSAGE_TYPES)}"
                    )
        
    except exceptions.WebsocketException as e:
        logger.error(f"INCOMMING MESSAGE ::: {message}")
        error_message = schemas.WebsocketMessage(
            type="BAD REQUEST",
            data={
                "detail": str(e)
            }
        )

        await websocket.send_json(error_message.model_dump())
        return

    except Exception:
        logger.exception("Error in websocket request")
        error_message = schemas.WebsocketMessage(
            type="SERVER ERROR",
            data={
                "detail": "Unable to process request at this time" 
            }
        )
        await websocket.send_json(error_message.model_dump())
        return

    except WebSocketDisconnect:
        logger.debug(f'Websocket connection: {connection_id} closed')
        WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)
        return

