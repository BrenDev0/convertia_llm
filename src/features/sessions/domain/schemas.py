from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Union

class UpdateEmbeddingSessionPayload(BaseModel):
    knowledge_id: UUID
    update: Dict[str, Union[str, int]]