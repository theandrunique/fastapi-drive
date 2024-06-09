from pydantic import BaseModel


class FileUploadedResponse(BaseModel):
    files: dict[str, str]
