import os
import json
from typing import Dict, Any, List
from datetime import datetime


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TASKS_ROOT = os.path.join(ROOT_DIR, "tasks", "state")
os.makedirs(TASKS_ROOT, exist_ok=True)

TASKS_FILE = os.path.join(TASKS_ROOT, "tasks.json")


def _load_tasks() -> List[Dict[str, Any]]:
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_tasks(tasks: List[Dict[str, Any]]) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def create_task(description: str, meta: Dict[str, Any] | None = None) -> str:
    tasks = _load_tasks()
    task_id = f"task_{len(tasks) + 1}"
    task = {
        "id": task_id,
        "description": description,
        "meta": meta or {},
        "created_at": datetime.utcnow().isoformat() + "Z",
        "status": "open",
    }
    tasks.append(task)
    _save_tasks(tasks)
    return task_id


def list_tasks() -> List[Dict[str, Any]]:
    return _load_tasks()
