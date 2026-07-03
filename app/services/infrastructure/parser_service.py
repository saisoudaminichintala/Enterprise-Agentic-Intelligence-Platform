class ParserService:
    """
    Extracts text from documents.

    Right now:
    - returns dummy parsed text.

    Later:
    - PDF parsing
    - DOCX parsing
    - TXT parsing
    """

    def parse_document(self, file_path: str) -> str:
        return f"Dummy parsed text from {file_path}"