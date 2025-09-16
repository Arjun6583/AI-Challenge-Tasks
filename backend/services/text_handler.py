from datetime import datetime
from pathlib import Path
from utils.helpers import ensure_dir, unique_stem
from utils.hash_utils import calculate_md5
from database.db import collection
from zoneinfo import ZoneInfo

def save_text_block(text: str, target_dir: Path, ext: str = ".txt") -> dict:
    try:
        ensure_dir(target_dir)
        ext = ext if ext.startswith(".") else f".{ext}"
        stem = unique_stem(prefix="text")
        dest = target_dir / f"{stem}{ext}"
        
        with dest.open("w", encoding="utf-8") as f:
            f.write(text)

        # calculate MD5 checksum
        file_md5 = calculate_md5(dest)
        metadata = {
            "path": str(dest.resolve()),
            "current_time": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
            "md5": file_md5,
            "filetype": "text"
        }

        collection.insert_one(metadata)

        # prepare response
        response = {
            "ai_response": "Give Text code is clean",
            "file_path": str(dest),
            "message": "Text block saved and metadata stored",
            "analysis": f"This is latest analysis from LLM {text[:30]}"
        }
        return response

    except Exception as e:
         return {"status": "error", "message": str(e)}
     