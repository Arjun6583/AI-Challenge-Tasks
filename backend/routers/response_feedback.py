from fastapi import APIRouter, Form
from services.response_feedback_service import save_feedback_service

router = APIRouter()

@router.post("/save_feedback/")
async def save_feedback(corrected: str = Form(...), file_path: str = Form(""), ai_response: str = Form("")):
    try:
        print(f"Received feedback: {corrected}")
        print(f"File Path: {file_path}")
        print(f"AI Response: {ai_response}")
        response = save_feedback_service(corrected, file_path, ai_response)
        return response
    except Exception as e:
        print(f"Error occurred while saving feedback: {e}")
        return {"status": "Error occurred while saving feedback"}

