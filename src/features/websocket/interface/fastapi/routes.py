import logging
from fastapi import APIRouter, Depends, WebSocket, status, WebSocketDisconnect
from uuid import UUID
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Websocket"]
)

router.websocket("/llm/{connection_id}")
async def async_ws_connect(
    websocket: WebSocket,
    connection_id: UUID
):
    params = websocket.query_params

    signature = params.get("x-signature")
    payload = params.get("x-payload")

    if not signature or payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    await websocket.accept()
    logger.debug(f"Websocket connection: {connection_id} closed")

    try:
        while True:
            message = await websocket.receive_json()
            logger.debug(f"INCOMMING MESSAGE ::: {message}")

    
    except WebSocketDisconnect:
        logger.debug(f'Websocket connection: {connection_id} closed')

