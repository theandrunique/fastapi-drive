import uuid
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class FileInDB(Base):
    __tablename__ = "files"
    
    id: Mapped[str] = mapped_column(unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str]