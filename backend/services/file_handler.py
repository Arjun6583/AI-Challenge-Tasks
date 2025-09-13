from pathlib import Path
import shutil
from backend.utils.utils import ensure_dir, safe_filename

def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    ensure_dir(target_dir)

    orig_name = safe_filename(uploaded_file.filename)
    dest = target_dir / orig_name

    # If file exists, append a counter
    counter = 1
    final_dest = dest
    while final_dest.exists():
        stem = Path(orig_name).stem
        suffix = Path(orig_name).suffix
        final_dest = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1

    with final_dest.open("wb") as f:
        shutil.copyfileobj(uploaded_file.file, f)  # uploaded_file.file is a file-like object

    return final_dest.resolve()
