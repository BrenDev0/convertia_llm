import os
from src.broker import AsyncHandler, BaseEvent
from src.http import AsyncHttpClient, generate_hmac_headers
from ...domain import UpdateEmbeddingStatusPayload


class UpdateEmeddingStatusHandler(AsyncHandler):
    def __init__(
        self,
        async_http_client: AsyncHttpClient
    ):
        self.__async_http_client = async_http_client

    async def handle(self, event):
        parsed_event = BaseEvent(**event)
        payload = UpdateEmbeddingStatusPayload(**parsed_event.payload)
        
        app_host = os.getenv("APP_HOST")

        headers = generate_hmac_headers()

        req_body = {
            "user_id": str(parsed_event.user_id),
            "status": payload.status,
            "knowledge_id": str(payload.knowledge_id)
        }

        await self.__async_http_client.request(
            endpoint=f"{app_host}/knowledge-base/embedding-status/{payload.knowledge_id}",
            method="PATCH",
            headers=headers,
            req_body=req_body
        )

