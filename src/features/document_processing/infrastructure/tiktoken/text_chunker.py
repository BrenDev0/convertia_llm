import tiktoken
from typing import List
from src.features.document_processing.domain.text_chunker import TextChunker
from  src.persistence.domain.entities import DocumentChunk

class TiktokenTextChunker(TextChunker):
    def chunk(self, text, max_tokens, token_overlap) -> List[DocumentChunk]:
        pass