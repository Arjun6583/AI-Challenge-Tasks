from pathlib import Path
from backend.utils.utils import ensure_dir, unique_stem

def save_text_block(text: str, target_dir: Path, ext: str = ".txt") -> Path:
    ensure_dir(target_dir)
    ext = ext if ext.startswith(".") else f".{ext}"
    stem = unique_stem(prefix="text")
    dest = target_dir / f"{stem}{ext}"
    
    with dest.open("w", encoding="utf-8") as f:
        f.write(text)
    return dest.resolve()
