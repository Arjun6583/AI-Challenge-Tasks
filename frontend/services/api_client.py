import requests

BACKEND_URL = "http://127.0.0.1:8000" 
LAST_ANALYSIS = None

def upload_file(file_name, file_bytes):
    try:
        files = {"file": (file_name, file_bytes)}

        requests.post(f"{BACKEND_URL}/summarize/", data={"text": "File Uploading"})
        response = requests.post(f"{BACKEND_URL}/upload_file/", files=files).json()
         
        global LAST_ANALYSIS  
        LAST_ANALYSIS = response["analysis"] if "analysis" in response else None 
        
        print(response)
        return response
    except Exception as e:
        raise Exception("File upload failed") from e
    

def save_text(query: str):
    try:
        requests.post(f"{BACKEND_URL}/summarize/", data={"text": "Text Code Sending"})
        
        response = requests.post(f"{BACKEND_URL}/save_text/", data={"text": query}).json()
        global LAST_ANALYSIS
        LAST_ANALYSIS = response["analysis"] if "analysis" in response else None
        
        print(response)
        return response
    except Exception as e:
        raise Exception("Text saving failed") from e

def get_analysis():
    try:
        print("Getting analysis:", LAST_ANALYSIS)
        return LAST_ANALYSIS
    except Exception as e:
        raise Exception("Analysis retrieval failed") from e 

def save_correct_feedback_response(corrected_response: str, file_path: str = "", ai_response: str = ""):
    try:
        response = requests.post(f"{BACKEND_URL}/save_feedback/", data={"corrected": corrected_response, "file_path": file_path, "ai_response": ai_response}).json()
        return response
    except Exception as e:
        raise Exception("Feedback saving failed") from e
