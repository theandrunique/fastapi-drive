from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile

from src.schemas import FileUploadedResponse
from src.services.s3_client import S3Session
from src.utils import get_file_category

router = APIRouter()


@router.post("/upload")
async def upload_file(files: list[UploadFile]) -> FileUploadedResponse:
    uploaded_files = {}

    for file in files:
        if file.content_type is None:
            raise HTTPException(status_code=400, detail="File content type is missing.")

        async with S3Session().client() as client:
            key = f"{get_file_category(file.content_type)}/{uuid4()}-{file.filename}"
            result = await client.put(key, await file.read())
            uploaded_files[file.filename] = result

    return FileUploadedResponse(files=uploaded_files)
