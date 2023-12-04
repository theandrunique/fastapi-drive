from enum import Enum
from pydantic import BaseModel


class FileType(Enum):
    track = "track"
    image = "image"
    video = "video"
    other = "other"


class UploadFileBase(BaseModel):
    name: str | None = None
    type: FileType


class UploadFileIn(UploadFileBase):
    pass


class UploadFileOut(UploadFileBase):
    pass
