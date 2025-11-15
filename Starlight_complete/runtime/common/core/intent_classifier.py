import re
from typing import Dict


def classify_intent(user_input: str) -> Dict[str, str]:
    """
    Simple rule-based intent classifier.
    """
    text = user_input.strip().lower()

    if not text:
        return {"kind": "chat", "reason": "empty input treated as casual chat"}

    if any(k in text for k in ["remember this", "save this", "store this"]):
        return {"kind": "memory", "reason": "contains a memory-saving cue phrase"}

    if any(k in text for k in ["todo", "to-do", "task:", "remind me", "schedule"]):
        return {"kind": "task", "reason": "contains task/reminder language"}

    if any(k in text for k in ["shutdown", "exit starlight", "reset context"]):
        return {"kind": "control", "reason": "user requested system control"}

    if text.endswith("?"):
        return {"kind": "chat", "reason": "user is asking a question"}

    return {"kind": "chat", "reason": "default chat intent"}
