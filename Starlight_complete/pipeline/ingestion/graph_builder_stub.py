import os
import sys
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Locate runtime/common so we can reuse StarLight's cloud_client
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
RUNTIME_COMMON = os.path.join(ROOT_DIR, "runtime", "common")
if RUNTIME_COMMON not in sys.path:
    sys.path.append(RUNTIME_COMMON)

try:
    from core import cloud_client  # type: ignore
except Exception:
    cloud_client = None

MEMORY_ROOT = os.path.join(ROOT_DIR, "memory")
EMBEDDINGS_DIR = os.path.join(MEMORY_ROOT, "embeddings", "episodic")


def _load_embedding_entry(entry_path: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON embedding entry from the embeddings directory.
    Returns None if loading fails.
    """
    try:
        with open(entry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return None


def build_memory_graph(target_memory_id: str) -> Dict[str, Any]:
    """
    Build a simplified memory graph for a given episodic memory.

    Returns a dictionary with:
    {
      "memory_id": <target_memory_id>,
      "related_memories": [
        {"memory_id": <id>, "connection_type": <type>, "score": <float>},
        ...
      ]
    }

    connection_type can be "temporal", "semantic", "same_context", etc.
    score is a float between 0-1 representing the strength of the connection.
    """
    if not os.path.isdir(EMBEDDINGS_DIR):
        return {
            "memory_id": target_memory_id,
            "related_memories": []
        }

    # Attempt to load the target memory entry
    target_file = os.path.join(EMBEDDINGS_DIR, f"{target_memory_id}.json")
    if not os.path.exists(target_file):
        return {
            "memory_id": target_memory_id,
            "related_memories": []
        }

    target_data = _load_embedding_entry(target_file)
    if not target_data:
        return {
            "memory_id": target_memory_id,
            "related_memories": []
        }

    target_embedding = target_data.get("embedding_vector", [])
    target_timestamp = target_data.get("timestamp", "")

    related_memories = []

    # Iterate over all other embeddings in the directory
    for filename in os.listdir(EMBEDDINGS_DIR):
        if not filename.endswith(".json"):
            continue

        other_id = filename.replace(".json", "")
        if other_id == target_memory_id:
            continue

        other_path = os.path.join(EMBEDDINGS_DIR, filename)
        other_data = _load_embedding_entry(other_path)
        if not other_data:
            continue

        # Use a simple scoring heuristic (can be improved with vector similarity, etc.)
        # For now, just return a dummy "semantic" connection
        related_memories.append({
            "memory_id": other_id,
            "connection_type": "semantic",
            "score": 0.5
        })

    return {
        "memory_id": target_memory_id,
        "related_memories": related_memories
    }
