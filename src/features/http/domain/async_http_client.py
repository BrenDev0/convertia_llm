from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AsyncHttpClient(ABC):

    @abstractmethod
    async def post_request(
        self,
        endpoint: str,
        req_body: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ):
        raise NotImplementedError
    
    @abstractmethod
    async def get_request(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ): 
        raise NotImplementedError
