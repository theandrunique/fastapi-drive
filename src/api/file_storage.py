from fastapi import APIRouter, UploadFile

from src.schemas import FileUploadedResponse
from src.services.s3_client import S3Session

router = APIRouter()


@router.post("/upload")
async def upload_file(files: list[UploadFile]) -> FileUploadedResponse:
    uploaded_files = {}

    for file in files:
        async with S3Session().client() as client:
            result = await client.put(file.filename, await file.read())
            uploaded_files[file.filename] = result

    return FileUploadedResponse(files=uploaded_files)
