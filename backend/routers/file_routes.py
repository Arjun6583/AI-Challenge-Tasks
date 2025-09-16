from fastapi import APIRouter, UploadFile
from pathlib import Path
from services.file_handler import save_uploaded_file

router = APIRouter()

FILE_DIR = Path("data/files")

@router.post("/upload_file/")
async def upload_file(file: UploadFile):
    try:
        response = save_uploaded_file(file, FILE_DIR) 
        response["status"] = "success"
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}
