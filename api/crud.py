from sqlalchemy.ext.asyncio import AsyncSession

from models import FileInDB


async def upload_file_in_db(
    session: AsyncSession,
    filename: str,
) -> FileInDB:
    file_in_db = FileInDB(name=filename)
    session.add(file_in_db)
    await session.commit()
    return file_in_db


async def get_file_from_db(
    session: AsyncSession,
    id: str,
) -> FileInDB:
    return await session.get(FileInDB, ident=id)
