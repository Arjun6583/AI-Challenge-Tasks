from fastapi import APIRouter, UploadFile, Form
from backend.services.text_handler import save_text_block
from backend.services.file_handler import save_uploaded_file
from backend.config import TEXT_DIR, FILE_DIR

router = APIRouter()

@router.post("/upload")
async def upload_file(
    code: str = Form(...), 
    file: UploadFile | None = None
):
    """
    Receive text/code and optional file from frontend.
    Returns saved file paths.
    """
    result = {}

    if code:
        text_path = save_text_block(code, target_dir=TEXT_DIR)
        result["text_path"] = str(text_path)

    if file:
        file_path = save_uploaded_file(file, target_dir=FILE_DIR)
        result["file_path"] = str(file_path)

    return result
