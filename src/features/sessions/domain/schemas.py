from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Union

class UpdateEmbeddingSessionPayload(BaseModel):
    knowledge_id: UUID
    session: Dict[str, Union[str, int]]