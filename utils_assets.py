# utils_assets.py
from __future__ import annotations
import re, time
from pathlib import Path
from typing import Optional

SAFE_ROOT = Path("assets/uploads")

def _slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.strip().lower())
    return re.sub(r"-+", "-", s).strip("-") or "file"

def ensure_dir(kind: str) -> Path:
    d = SAFE_ROOT / kind
    d.mkdir(parents=True, exist_ok=True)
    return d

def save_upload(up_file, kind: str, name_hint: Optional[str] = None) -> str:
    target_dir = ensure_dir(kind)
    ext = ""
    if "." in up_file.name:
        ext = "." + up_file.name.rsplit(".", 1)[-1].lower()
    base = _slug(name_hint or up_file.name.rsplit(".", 1)[0])
    stamp = time.strftime("%Y%m%d_%H%M%S")
    fname = f"{base}_{stamp}{ext}"
    path = target_dir / fname
    path.write_bytes(up_file.read())
    return path.as_posix()
