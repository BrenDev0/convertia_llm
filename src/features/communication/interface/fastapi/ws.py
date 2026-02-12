import logging
from uuid import UUID
from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect
from src.websocket.container import WebsocketConnectionsContainer
from src.websocket.domain import schemas
from src.security.hmac import verify_hmac_ws


logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Websocket"]
)

@router.websocket("/communications/{connection_id}")
async def async_ws_connect(
    websocket: WebSocket,
    connection_id: UUID
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
    logger.debug(f"Websocket connection: {connection_id} registerd")

    try:
        while True:
            message = await websocket.receive_json()

    except WebSocketDisconnect:
        logger.debug(f'Websocket connection: {connection_id} closed')
        WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)
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

    

