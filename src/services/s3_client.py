from contextlib import asynccontextmanager
from aiobotocore.session import get_session

from .base.base_s3_client import BaseS3Client


from src.config import config


class S3Session:
    def __init__(self) -> None:
        self.session = get_session()
        pass

    @asynccontextmanager
    async def client(self):
        async with self.session.create_client(
            "s3",
            aws_access_key_id=config.S3_ACCESS_KEY,
            aws_secret_access_key=config.S3_SECRET_KEY,
            endpoint_url=config.S3_ENDPOINT_URL,
        ) as client:
            yield S3Client(client)


class S3Client(BaseS3Client):
    def __init__(self, client) -> None:
        self.client = client

    async def get(self, key: str) -> bytes:
        return await self.client.get_object(Bucket=config.S3_BUCKET_NAME, Key=key)

    async def put(self, key: str, data: bytes) -> str:
        await self.client.put_object(Bucket=config.S3_BUCKET_NAME, Key=key, Body=data)
        return f"{config.S3_BUCKET_URL}/{key}"

    async def delete(self, key: str):
        return await self.client.delete_object(Bucket=config.S3_BUCKET_NAME, Key=key)
