import os
from src.broker.domain import base_event, handlers
from src.features.http.domain.async_http_client import AsyncHttpClient
from src.features.knowledge_base.domain.schemas import UpdateEmbeddingStatusPayload
from src.features.http.utils.hmac import generate_hmac_headers

class UpdateEmeddingStatus(handlers.AsyncHandler):
    def __init__(
        self,
        async_http_client: AsyncHttpClient
    ):
        self.__async_http_client = async_http_client

    async def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        payload = UpdateEmbeddingStatusPayload(**parsed_event.payload)
        
        app_host = os.getenv("APP_HOST")

        headers = generate_hmac_headers()

        req_body = {
            "user_id": str(parsed_event.user_id),
            "status": payload.is_embedded,
            "knowledge_id": str(payload.knowledge_id)
        }

        await self.__async_http_client.post_request(
            endpoint=f"{app_host}/knowledge-base/embedding-status/{payload.knowledge_id}",
            headers=headers,
            req_body=req_body
        )

