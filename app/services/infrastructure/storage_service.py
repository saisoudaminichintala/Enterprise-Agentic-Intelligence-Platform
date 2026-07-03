import os
from fastapi import UploadFile


class StorageService:
    """
    Saves uploaded files.

    Later:
    - local storage can be replaced with S3/Azure Blob/GCS.
    """

    def __init__(self, upload_dir: str = "uploaded_docs"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_file(self, file: UploadFile) -> str:
        file_path = os.path.join(self.upload_dir, file.filename)

        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        return file_path