from abc import ABC, abstractmethod

class PdfProcessor(ABC):
    @abstractmethod
    def process(
    self, 
    file_bytes: bytes
) -> str:
       raise NotImplementedError