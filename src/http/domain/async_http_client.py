from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AsyncHttpClient(ABC):

    @abstractmethod
    async def request(
        self,
        endpoint: str,
        method: str, 
        req_body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        raise NotImplementedError
    
   