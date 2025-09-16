from fastapi import APIRouter, Form
from pathlib import Path
from services.text_handler import save_text_block

router = APIRouter()

TEXT_DIR = Path("data/texts")

@router.post("/save_text/")
async def save_text(text: str = Form(...)):
    try:
        response = save_text_block(text, TEXT_DIR) 
        print("Analysis Response:", response)
        response["status"] = "success"
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}
