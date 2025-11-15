import os
import sys
import json
from typing import Dict, Any, List
from datetime import datetime

# Locate runtime/common so we can reuse Starlight's cloud_client
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
RUNTIME_COMMON = os.path.join(ROOT_DIR, "runtime", "common")

if RUNTIME_COMMON not in sys.path:
    sys.path.append(RUNTIME_COMMON)

try:
    from core import cloud_client  # type: ignore
except Exception:
    cloud_client = None  # type: ignore


MEMORY_ROOT = os.path.join(ROOT_DIR, "memory")
INBOX_DIR = os.path.join(MEMORY_ROOT, "inbox")
EMBED_DIR = os.path.join(MEMORY_ROOT, "embeddings", "episodic")

os.makedirs(INBOX_DIR, exist_ok=True)
os.makedirs(EMBED_DIR, exist_ok=True)


def _load_json(path: str) -> Dict[str, Any] | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _embedding_path(mem_id: str) -> str:
    return os.path.join(EMBED_DIR, f"{mem_id}.json")


def _list_inbox() -> List[str]:
    return [
        os.path.join(INBOX_DIR, f)
        for f in os.listdir(INBOX_DIR)
        if f.endswith(".json")
    ]


def encode_new_memories() -> None:
    if cloud_client is None or not cloud_client.is_cloud_available():
        print("[memory_encoder] Cloud embedding endpoint unavailable; skipping.")
        return

    inbox_files = _list_inbox()
    if not inbox_files:
        print("[memory_encoder] No inbox memories to encode.")
        return

    texts: List[str] = []
    items: List[Dict[str, Any]] = []

    for path in inbox_files:
        data = _load_json(path)
        if not data:
            continue
        mem_id = data.get("id") or os.path.splitext(os.path.basename(path))[0]
        text = data.get("text", "").strip()
        if not text:
            continue
        texts.append(text)
        data["id"] = mem_id
        items.append(data)

    if not texts:
        print("[memory_encoder] No valid texts found in inbox.")
        return

    print(f"[memory_encoder] Requesting embeddings for {len(texts)} memories...")
    result = cloud_client.cloud_embed(texts)  # type: ignore[attr-defined]
    embeddings = result.get("embeddings") or []

    if len(embeddings) != len(items):
        print("[memory_encoder] WARNING: embedding count mismatch; aborting.")
        return

    for item, emb in zip(items, embeddings):
        mem_id = item["id"]
        out = {
            "id": mem_id,
            "embedding": emb,
            "meta": item.get("meta", {}),
            "source_timestamp": item.get("timestamp"),
            "encoded_at": datetime.utcnow().isoformat() + "Z",
        }
        out_path = _embedding_path(mem_id)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"[memory_encoder] wrote embedding → {out_path}")

    print("[memory_encoder] Done.")


if __name__ == "__main__":
    encode_new_memories()
