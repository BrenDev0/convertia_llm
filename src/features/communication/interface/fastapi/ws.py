import logging
import os
from src.di import Injector
from uuid import UUID, uuid4
from pydantic import ValidationError
from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect, Depends
from src.websocket import WebsocketConnectionsContainer, WebsocketMessage, WebsocketException
from src.security import verify_hmac_ws
from src.http import generate_hmac_headers, AsyncHttpClient
from src.persistence import NotFoundException, SessionRepository
from src.broker import ChatEvent, ChatsProducer
from src.features.messages.domain import CreateMessagePayload
from src.features.llm.domain import InvokeAgentPayload
from ...domain import IncommingMessageData

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Websocket"]
)

def get_injector(
    websocket: WebSocket
):
    """
    Use with Depends() to get di injector
    """

    return websocket.app.state.injector

async def get_agent_config(
    agent_id: UUID,
    injector: Injector
    ):
    """
    check if agent config is in redis if not get it from 
    main server and store in redis

    args: 
    agent id(from request)
    injector: Injector class from src.di passed from app state. 
    This must be the injector used in the deployment

    returns:
    agent_id: UUID
    system_prompt: str
    temperature: float
    transcripts: bool
    """

    session_repository: SessionRepository = injector.resolve(SessionRepository)
    key = f"{agent_id}_settings"
    session = session_repository.get_session(key)

    if not session:
        http_client = injector.resolve(AsyncHttpClient)
        try:
            app_host = os.getenv("APP_HOST")

            headers = generate_hmac_headers()
            
            return await http_client.request(
                endpoint=f"{app_host}/agent-settings/{agent_id}",
                method="GET",
                headers=headers
            )
        
        except NotFoundException:
            raise WebsocketException(f"No agent settings found for agent with id: {agent_id}")
        
        except Exception:
            raise

    return session

@router.websocket("/communications/{connection_id}")
async def async_ws_connect(
    websocket: WebSocket,
    connection_id: UUID,
    injector: Injector = Depends(get_injector)
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
            parsed_message = WebsocketMessage(**message)

            match(parsed_message.type.upper()):
                case "MESSAGE":
                    data = IncommingMessageData(**parsed_message.data)
                    agent_config = get_agent_config(
                        agent_id=data.agent_id,
                        injector=injector
                    )

                    create_message_payload = CreateMessagePayload(
                        type="human",
                        text=data.input,
                        transctipts=agent_config["transcripts"]
                    )

                    invoke_agent_payload = InvokeAgentPayload(
                        input=data.input,
                        prompt=agent_config["prompt"],
                        max_tokens=agent_config["max_tokens"],
                        temperature=agent_config["temperature"],
                        transcripts=agent_config["transcripts"]
                    )

                    chat_event = ChatEvent(
                        event_id=uuid4(),
                        connection_id=connection_id,
                        agent_id=data.agent_id
                    )

                    chat_event.payload = create_message_payload.model_dump()

                    chat_producer: ChatsProducer = injector.resolve(ChatsProducer)
                    chat_producer.publish(
                        routing_key="chats.history.update",
                        event=chat_event
                    )


                    chat_event.payload = invoke_agent_payload.model_dump()
                    chat_producer.publish(
                        routing_key="chats.llm.client.invoke",
                        event=chat_event
                    )

                case _:
                    raise WebsocketException(f"Invalid message type: {parsed_message.type}")
                



    except WebSocketDisconnect:
        logger.debug(f'Websocket connection: {connection_id} closed')
        WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)
        return
    

    
    except ValidationError as e:
        logger.error(f"Invalid message format: {e}")
        error_message = WebsocketMessage(
            type="BAD_REQUEST",
            data={
                "detail": "Invalid message format",
                "errors": e.errors()
            }
        )
        await websocket.send_json(error_message.model_dump())

    except WebsocketException as e:
        logger.error(f"Invalid message type {parsed_message.type}")
        error_message = WebsocketMessage(
            type="BAD_REQUEST",
            data={
                "detail": str(e) 
            }
        )
        await websocket.send_json(error_message.model_dump())
        
    except Exception:
        logger.exception("Error in websocket request")
        error_message = WebsocketMessage(
            type="SERVER ERROR",
            data={
                "detail": "Unable to process request at this time" 
            }
        )
        await websocket.send_json(error_message.model_dump())
        return

    

