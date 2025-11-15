from typing import Dict, Any, Optional


def local_fallback_reply(
    user_input: str,
    intent: Dict[str, Any],
    context: Dict[str, Any],
    cloud_available: bool,
) -> str:
    """
    Local-only logic for when cloud is offline or skipped.
    Very lightweight fallback.
    """
    if not cloud_available:
        return (
            "I'm Starlight running locally (no cloud access). "
            f"I received: {user_input!r}. "
            "When cloud reconnects, I'll reason more deeply."
        )

    if intent.get("kind") == "memory":
        return (
            "I'll treat this as something to remember and keep it locally until "
            "the full memory pipeline is online."
        )

    return (
        "I'm Starlight's local fallback brain. I've logged what you said and "
        "will sync it with the cloud brain when available."
    )


def merge_response(
    user_input: str,
    intent: Dict[str, Any],
    context: Dict[str, Any],
    cloud_response: Optional[Dict[str, Any]],
    local_reply: Optional[str],
    used_cloud: bool,
    timestamp: str,
) -> Dict[str, Any]:
    """
    Combine cloud reasoning + local fallback into one standardized record.
    """
    if cloud_response and isinstance(cloud_response, dict):
        reply_text = cloud_response.get("reply") or local_reply or ""
        proposed_tasks = cloud_response.get("proposed_tasks") or []
        proposed_memories = cloud_response.get("proposed_memories") or []
    else:
        reply_text = local_reply or ""
        proposed_tasks = []
        proposed_memories = []

    return {
        "timestamp": timestamp,
        "user_input": user_input,
        "intent": intent,
        "context_snapshot": {
            "memory_summary": context.get("memory_summary", {}),
        },
        "used_cloud": used_cloud,
        "reply": reply_text,
        "proposed_tasks": proposed_tasks,
        "proposed_memories": proposed_memories,
    }
