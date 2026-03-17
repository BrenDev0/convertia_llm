import os
from src.broker import AsyncHandler, ChatsProducer, ChatEvent
from src.http import AsyncHttpClient, generate_hmac_headers
from ...domain import CreateMessagePayload

class CreateMessageHandler(AsyncHandler):
    def __init__(
        self,
        async_http_client: AsyncHttpClient,
        chats_producer: ChatsProducer
    ):
        self.__async_http_client = async_http_client
        self.__chats_producer = chats_producer

    async def handle(self, event):
        parsed_event = ChatEvent(**event)
        payload = CreateMessagePayload(**parsed_event.payload)

        app_host = os.getenv("APP_HOST")

        headers = generate_hmac_headers()

        req_body = {
            "chat_id": str(parsed_event.connection_id),
            "type": payload.type,
            "text": payload.text
        }

        await self.__async_http_client.request(
            endpoint=f"{app_host}/messages/",
            method="POST",
            headers=headers,
            req_body=req_body
        )

        await self.__chats_producer.publish(
            routing_key="",
            event=parsed_event
        )