import hashlib
from pathlib import Path

def calculate_md5(file_path: Path) -> str:
    """Calculate MD5 checksum of a file."""
    try:
        hash_md5 = hashlib.md5()
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):  # read in chunks
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        raise Exception(f"Failed to calculate MD5 for {file_path}") from e
