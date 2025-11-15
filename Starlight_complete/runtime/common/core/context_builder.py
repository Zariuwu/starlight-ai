import os
import json
from typing import Dict, Any, List


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_DIR = os.path.join(ROOT_DIR, "logs", "runtime")
SESSION_LOG = os.path.join(LOG_DIR, "session_log.jsonl")


def _load_recent_events(limit: int = 10) -> List[Dict[str, Any]]:
    events = []

    if not os.path.exists(SESSION_LOG):
        return events

    try:
        with open(SESSION_LOG, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    events.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    except Exception:
        return []

    return events[-limit:]


def _summarize_memory(runtime_root: str) -> Dict[str, Any]:
    memory_root = os.path.join(runtime_root, "memory")
    inbox_dir = os.path.join(memory_root, "inbox")
    graph_nodes_dir = os.path.join(memory_root, "graph", "nodes")

    inbox_count = len([f for f in os.listdir(inbox_dir)]) if os.path.isdir(inbox_dir) else 0
    graph_count = len([f for f in os.listdir(graph_nodes_dir)]) if os.path.isdir(graph_nodes_dir) else 0

    return {
        "inbox_count": inbox_count,
        "graph_node_count": graph_count
    }


def build_context(user_input: str, intent: Dict[str, Any], runtime_root: str) -> Dict[str, Any]:
    recent_events = _load_recent_events(limit=8)
    memory_summary = _summarize_memory(runtime_root)

    return {
        "user_input": user_input,
        "intent": intent,
        "recent_events": recent_events,
        "memory_summary": memory_summary,
    }
