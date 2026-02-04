import httpx
import json
from typing import Dict, Any, Optional
from src.features.http.domain.async_http_client import AsyncHttpClient

class HttpxAsyncHttpClient(AsyncHttpClient):
    async def post_request(
        self,
        endpoint: str, 
        req_body: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=endpoint,
                headers=headers or {},
                json=req_body
            )
            response.raise_for_status()
            
            return response

    async def get_request(
        self, 
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=endpoint,
                headers=headers or {}
            )

            response.raise_for_status()

            return response