import os
import sys
import json
from typing import Dict, List, Any, Optional

# Locate the root directory for memory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
PROJECT_ROOT = os.path.dirname(RUNTIME_ROOT)
MEMORY_ROOT = os.path.join(PROJECT_ROOT, "memory")
EMBEDDINGS_DIR = os.path.join(MEMORY_ROOT, "embeddings", "episodic")


def _load_json(path: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON file from the given path.
    Returns None if loading fails.
    """
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def retrieve_memories(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve relevant memories based on a query string.

    For now, this is a very simple stub that returns the most recent memories
    in the EMBEDDINGS_DIR folder. In a production system, you would:
    1. Encode the query string into an embedding vector
    2. Compare the query embedding against stored memory embeddings
    3. Return the top_k most similar memories based on cosine similarity

    Returns a list of dictionaries, each containing:
    {
      "memory_id": <id>,
      "text": <original text>,
      "timestamp": <timestamp>,
      "embedding_vector": <vector> (optional)
    }
    """
    if not os.path.isdir(EMBEDDINGS_DIR):
        return []

    # Collect all memory files
    memory_files = []
    for filename in os.listdir(EMBEDDINGS_DIR):
        if filename.endswith(".json"):
            memory_id = filename.replace(".json", "")
            file_path = os.path.join(EMBEDDINGS_DIR, filename)
            data = _load_json(file_path)
            if data:
                data["memory_id"] = memory_id
                memory_files.append(data)

    # Sort by timestamp (descending), then return top_k
    memory_files.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return memory_files[:top_k]


def retrieve_by_id(memory_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single memory by its ID.

    Returns the memory data dictionary if found, or None if not found.
    """
    if not os.path.isdir(EMBEDDINGS_DIR):
        return None

    file_path = os.path.join(EMBEDDINGS_DIR, f"{memory_id}.json")
    data = _load_json(file_path)
    if data:
        data["memory_id"] = memory_id
    return data


def retrieve_related(memory_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve memories related to a specific memory ID.

    This is a stub that simply returns the top_k most recent memories
    (excluding the given memory_id). In production, this would use the
    memory graph to find semantically or contextually related memories.
    """
    if not os.path.isdir(EMBEDDINGS_DIR):
        return []

    memory_files = []
    for filename in os.listdir(EMBEDDINGS_DIR):
        if filename.endswith(".json"):
            mid = filename.replace(".json", "")
            if mid == memory_id:
                continue
            file_path = os.path.join(EMBEDDINGS_DIR, filename)
            data = _load_json(file_path)
            if data:
                data["memory_id"] = mid
                memory_files.append(data)

    memory_files.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return memory_files[:top_k]
