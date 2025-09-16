from database.db import db 

def save_feedback_service(corrected: str, file_path: str, ai_response: str) -> dict:
    try:
        collection = db["feedback"]
        feedback_data = {
            "corrected_response": corrected,
            "file_path": file_path,
            "ai_response": ai_response
        }

        collection.insert_one(feedback_data)
        print("Feedback saved:", feedback_data)
        return {"status": "Feedback saved successfully"} 

    except Exception as e:
        print("Error saving feedback:", str(e))
        return {"status": "error", "message": str(e)}
