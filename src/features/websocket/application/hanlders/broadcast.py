import logging
from src.broker.domain import base_event, handlers
from src.features.websocket.container import WebsocketConnectionsContainer

logger = logging.getLogger(__name__)

class BroadcastHandler(handlers.AsyncHandler):
    def __init__(self):
        pass

    async def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)

        websocket = WebsocketConnectionsContainer.resolve_connection(
            connection_id=parsed_event.connection_id
        )

        if not websocket:
            logger.debug(f"Unable to broadcast message. Connection with id: {parsed_event.connection_id} not found")
            return 
        

        try:
            await websocket.send_json(parsed_event.payload)
        
        except Exception as e:
            if "closed" in str(e).lower() or "disconnect" in str(e).lower():
                logger.debug(f"Connection {parsed_event.connection_id} disconnected")
                return
            
            return 

        


