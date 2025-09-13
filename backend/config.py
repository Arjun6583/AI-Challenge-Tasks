from pathlib import Path

BASE_DIR = Path(__file__).parent / "storage"
TEXT_DIR = BASE_DIR / "text_storage"
FILE_DIR = BASE_DIR / "files_storage"

# Ensure directories exist
TEXT_DIR.mkdir(parents=True, exist_ok=True)
FILE_DIR.mkdir(parents=True, exist_ok=True)
