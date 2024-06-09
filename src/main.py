from fastapi import FastAPI
from src.api.file_storage import router as file_storage_router

app = FastAPI()
app.include_router(file_storage_router, prefix="/file", tags=["File Storage"])
