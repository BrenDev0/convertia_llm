import httpx
import json
from typing import Dict, Any, Optional
from src.http.domain.async_http_client import AsyncHttpClient

class HttpxAsyncHttpClient(AsyncHttpClient):
    async def request(
        self,
        endpoint: str,
        method: str, 
        req_body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=endpoint,
                headers=headers or {},
                json=req_body or {}
            )

            response.raise_for_status()
            return response