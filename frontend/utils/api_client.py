import requests

BACKEND_URL = "http://127.0.0.1:8000"

def send_upload(code: str, uploaded_file=None):
    """
    Send code and optional file to backend FastAPI.
    """
    files = {}
    data = {"code": code}

    if uploaded_file:
        files["file"] = (uploaded_file.name, uploaded_file.getvalue())

    try:
        resp = requests.post(f"{BACKEND_URL}/upload", data=data, files=files)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
