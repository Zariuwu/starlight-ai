from .retrieval import search_memories


def warm_memory(query: str = "hello"):
    """Warm the retrieval system on boot."""
    try:
        _ = search_memories(query, top_k=3)
        print("[boot] Memory retrieval warmed.")
    except Exception:
        print("[boot] Retrieval warm failed.")
