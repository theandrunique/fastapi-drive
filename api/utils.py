from typing import Annotated

from fastapi import Depends, HTTPException, Path, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles

from core.config import settings
from models import FileInDB
from .crud import upload_file_in_db
from models import db_helper


async def upload_file_to_dir(
    file: UploadFile,
    session: AsyncSession
):
    file_in_db = await upload_file_in_db(
        session=session,
        filename=file.filename,
    )
    async with aiofiles.open(
        f"{settings.STORAGE_DIR_NAME}/{file_in_db.id}",
        "wb",
    ) as nf:
        await nf.write(await file.read())

    return {
        "id": file_in_db.id,
        "url": f"/{file_in_db.id}",
        "filename": file.filename,
    }


async def get_file_by_id(
    file_id: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> FileInDB:
    file = await session.get(FileInDB, ident=file_id)
    if file:
        return file

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"file {file_id} not found",
    )
