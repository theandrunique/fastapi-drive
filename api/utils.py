from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from .crud import upload_file_in_db


async def upload_file_to_dir(
    file: UploadFile,
    session: AsyncSession,
    dir: str,
):
    file_in_db = await upload_file_in_db(
        session=session,
        filename=file.filename,
    )
    with open(f"{settings.STORAGE_DIR_NAME}/{dir}/{file_in_db.id}", "wb") as nf:
        nf.write(await file.read()) 
    return {
        "url": f"/{dir}/{file_in_db.id}",
        "filename": file.filename,
    }