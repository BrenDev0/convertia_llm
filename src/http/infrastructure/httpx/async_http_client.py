import httpx
from httpx import HTTPStatusError
from typing import Dict, Any, Optional
from src.persistence import NotFoundException
from ...domain import AsyncHttpClient

class HttpxAsyncHttpClient(AsyncHttpClient):
    async def request(
        self,
        endpoint: str,
        method: str, 
        req_body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=endpoint,
                    headers=headers or {},
                    json=req_body or {}
                )

                response.raise_for_status()
                return response
            
        except HTTPStatusError as e:
            status_code = e.response.status_code
            if int(status_code) == 404:
                raise NotFoundException()
            
            raise e