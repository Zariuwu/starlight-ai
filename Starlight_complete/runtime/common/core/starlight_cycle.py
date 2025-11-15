import time
from typing import Dict, Any, List

from .intent_classifier import classify_intent
from .context_builder import build_context
from .response_merger import merge_response, local_fallback_reply
from .cloud_client import cloud_reason
from ..memory import retrieval


def starlight_reason(message: str, system_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full hybrid reasoning loop:
    1. Classify intent
    2. Retrieve memory (episodic + semantic)
    3. Build context package
    4. Cloud reasoning
    5. Merge with memory + local fallback
    """

    intent = classify_intent(message)
    memories = retrieval.search_memories(message, top_k=5)
    context = build_context(message, intent, memories)

    cloud_out = cloud_reason(context)
    final = merge_response(
        user_message=message,
        cloud_message=cloud_out,
        intent=intent,
        memories=memories,
    )

    return {
        "intent": intent,
        "memories_used": len(memories),
        "response": final,
        "timestamp": time.time()
    }
