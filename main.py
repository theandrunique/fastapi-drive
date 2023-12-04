from fastapi import FastAPI
from api.views import router

app = FastAPI()
app.include_router(router)