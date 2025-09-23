from datetime import datetime
from pathlib import Path
import shutil
from utils.helpers import ensure_dir, safe_filename
from utils.hash_utils import calculate_md5
from database.db import collection
from datetime import datetime
from zoneinfo import ZoneInfo 
import services.llm_service as llm_service

def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    """Save uploaded file and store metadata in MongoDB."""
    try:
        ensure_dir(target_dir)

        orig_name = safe_filename(uploaded_file.filename)
        dest = target_dir / orig_name

        counter = 1
        final_dest = dest
        while final_dest.exists():
            stem = Path(orig_name).stem
            suffix = Path(orig_name).suffix
            final_dest = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        with final_dest.open("wb") as f:
            shutil.copyfileobj(uploaded_file.file, f) 
            
        content = None
        with final_dest.open("r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        #call api to get file type 
        code_blocks = llm_service.llm_guard_code_object._extract_code_blocks(content)
        code_blocks = [content]
        results = llm_service.llm_guard_code_object._pipeline(code_blocks)
        language_detect = results[0][0]['label'] 
        
        file_md5 = calculate_md5(final_dest)
        metadata = {
            "path": str(final_dest.resolve()),
            "created_at": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
            "md5": file_md5,
            "filetype": "malware",
            "language": language_detect
        }

        collection.insert_one(metadata) 
        #call to LLM to predict file content and there type
        #after call to LLM file is error or not 
        respose = {
            "message": "File saved and metadata stored",
            "analysis": f"This is latest analysis from LLm {uploaded_file.filename}",
            "file_path": str(final_dest.resolve()),
            "ai_response": f"Langauge Detect {language_detect}"
        }
        print(respose)
        return respose
    except Exception as e:
        raise Exception("Failed to save uploaded file and process file") from e
