from pathlib import Path
from pypdf import PdfReader
from docx import Document


class ParserService:
    def parse_document(self, file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self._parse_pdf(file_path)

        if extension == ".docx":
            return self._parse_docx(file_path)

        if extension == ".txt":
            return self._parse_txt(file_path)

        raise ValueError(f"Unsupported file type: {extension}")

    def _parse_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        return "\n".join(text_parts)

    def _parse_docx(self, file_path: str) -> str:
        document = Document(file_path)
        return "\n".join(
            paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()
        )

    def _parse_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()