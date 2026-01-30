import tiktoken
from typing import List, Dict, Any
from uuid import uuid4
from src.features.document_processing.domain.text_chunker import TextChunker
from src.persistence.domain.entities import DocumentChunk


class TiktokenTextChunker(TextChunker):
    def __init__(self, model_name: str = "text-embedding-3-large"):
        self.encoding = tiktoken.encoding_for_model(model_name)

    def chunk(
        self,
        text: str,
        metadata: Dict[str, Any],
        max_tokens: int = 1000,
        overlap_tokens: int = 200
    ) -> List[DocumentChunk]:

        tokens = self.encoding.encode(text)

        step = max_tokens - overlap_tokens

        chunks: List[DocumentChunk] = []

        for start in range(0, len(tokens), step):
            end = start + max_tokens
            chunk_tokens = tokens[start:end]

            if not chunk_tokens:
                break

            chunk_text = self.encoding.decode(chunk_tokens)

            chunks.append(
                DocumentChunk(
                    chunk_id=uuid4(),
                    content=chunk_text,
                    metadata=metadata
                    
                )
            )

        return chunks
