from pathlib import Path
import re
from datetime import datetime
import uuid

SAFE_CHARS_RE = re.compile(r"[^A-Za-z0-9._-]+")

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def safe_filename(name: str) -> str:
    """Turn any filename into a safe, portable one."""
    name = name.strip().replace(" ", "_")
    name = SAFE_CHARS_RE.sub("", name)
    return name or "file"

def unique_stem(prefix: str | None = None) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    rand = uuid.uuid4().hex[:8]
    base = f"{ts}-{rand}"
    return f"{prefix}-{base}" if prefix else base
