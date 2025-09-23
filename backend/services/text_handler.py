from datetime import datetime
from pathlib import Path
from utils.helpers import ensure_dir, unique_stem
from utils.hash_utils import calculate_md5
from database.db import collection
from zoneinfo import ZoneInfo 
import services.llm_service as llm_service

def save_text_block(text: str, target_dir: Path, ext: str = ".txt") -> dict:
    try:
        ensure_dir(target_dir)
        ext = ext if ext.startswith(".") else f".{ext}"
        stem = unique_stem(prefix="text")
        dest = target_dir / f"{stem}{ext}"
        
        with dest.open("w", encoding="utf-8") as f:
            f.write(text)

        content = text
        #call api to get file type 
        code_blocks = llm_service.llm_guard_code_object._extract_code_blocks(content)
        code_blocks = [content]
        results = llm_service.llm_guard_code_object._pipeline(code_blocks)
        language_detect = results[0][0]['label'] 
        
        # calculate MD5 checksum
        file_md5 = calculate_md5(dest)
        metadata = {
            "path": str(dest.resolve()),
            "current_time": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
            "md5": file_md5,
            "filetype": "text",
            "language": language_detect
        }

        collection.insert_one(metadata)

        # prepare response
        response = {
            "ai_response": f"Language Detect {language_detect}",
            "file_path": str(dest),
            "message": "Text block saved and metadata stored",
            "analysis": f"This is latest analysis from LLM {text[:30]}"
        }
        return response

    except Exception as e:
         return {"status": "error", "message": str(e)}
     
