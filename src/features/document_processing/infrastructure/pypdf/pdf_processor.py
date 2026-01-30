import io
from pypdf import PdfReader
from src.features.document_processing.domain.pdf_processor import PdfProcessor

class PypdfProcessor(PdfProcessor):
    def process(self, file_bytes):
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        return text