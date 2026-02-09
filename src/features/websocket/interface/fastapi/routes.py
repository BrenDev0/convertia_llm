import logging
import os
import hmac
import hashlib
import time
from fastapi import APIRouter, Depends, WebSocket, status, WebSocketDisconnect
from src.features.websocket.container import WebsocketConnectionsContainer
from uuid import UUID
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

@router.websocket("/llm/{connection_id}")
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
    logger.debug(f"Websocket connection: {connection_id} closed")

    try:
        while True:
            message = await websocket.receive_json()
            logger.debug(f"INCOMMING MESSAGE ::: {message}")

    
    except WebSocketDisconnect:
        logger.debug(f'Websocket connection: {connection_id} closed')

