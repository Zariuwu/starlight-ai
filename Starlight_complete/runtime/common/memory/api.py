import os
import json
from typing import Dict, Any
from datetime import datetime


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MEMORY_ROOT = os.path.join(ROOT_DIR, "memory")
INBOX_DIR = os.path.join(MEMORY_ROOT, "inbox")

os.makedirs(INBOX_DIR, exist_ok=True)


def add_memory(text: str, meta: Dict[str, Any] | None = None) -> str:
    """
    Writes a JSON memory into memory/inbox/.
    Will be ingested + embedded later.
    """
    mem_id = f"mem_{datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')}"
    obj = {
        "id": mem_id,
        "text": text,
        "meta": meta or {},
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    path = os.path.join(INBOX_DIR, f"{mem_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return mem_id
