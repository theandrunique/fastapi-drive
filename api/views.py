import os
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Path,
    UploadFile,
    HTTPException,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from models import FileInDB

from .crud import delete_field_from_db, get_file_from_db
from .schemas import FileType
from models import db_helper
from .utils import get_file_by_id, upload_file_to_dir

router = APIRouter()


@router.post("/upload/")
async def upload_file(
    file: Annotated[UploadFile, File()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await upload_file_to_dir(file=file, session=session, dir="other")


@router.post("/upload-track/")
async def upload_track(
    file: Annotated[UploadFile, File()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await upload_file_to_dir(file=file, session=session, dir="track")


@router.post("/upload-image/")
async def upload_file(
    file: Annotated[UploadFile, File()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await upload_file_to_dir(file=file, session=session, dir="image")


@router.post("/upload-video/")
async def upload_file(
    file: Annotated[UploadFile, File()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await upload_file_to_dir(file=file, session=session, dir="video")


@router.get("/{filetype}/{file_id}")
async def get_file(
    filetype: Annotated[FileType, Path],
    file_id: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    file_from_db = await get_file_from_db(session=session, id=file_id)
    if not file_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"file {file_id} not found"
        )

    return FileResponse(
        path=f"{settings.STORAGE_DIR_NAME}/{filetype.value}/{file_id}",
        filename=file_from_db.name,
    )


@router.delete("/{filetype}/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    filetype: Annotated[FileType, Path],
    file_id: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    file_from_db: FileInDB = Depends(get_file_by_id),
):
    if not os.path.exists(f"{settings.STORAGE_DIR_NAME}/{filetype.value}/{file_id}"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"file {file_id} not found"
        )
    await delete_field_from_db(session=session, file=file_from_db)
    os.remove(f"{settings.STORAGE_DIR_NAME}/{filetype.value}/{file_id}")
