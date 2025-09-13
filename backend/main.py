from fastapi import FastAPI
from backend.routers import upload

app = FastAPI(title="File & Code Upload API")

app.include_router(upload.router)
